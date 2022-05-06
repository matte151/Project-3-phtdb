from tabnanny import check
from django.shortcuts import redirect, render
import requests

import uuid
import boto3

from .models import Pet, Photo, CheckupPhoto, User, Vet, Profile, Checkup, Prescription
from .forms import CheckupForm

from django.http import HttpResponse
from django.db import models

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

def is_vet(user):
    return user.groups.filter(name='vet').exists()

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'phtdb'

APIKEY='GvkdrK5ufYyoOw6mxulvwIzkqpagIwbTHdbeDjUv'
url = f'https://api.fda.gov/drug/label.json?api_key={APIKEY}&search=advil'
response = requests.get(url)
data = response.json()

# Note the URL is only ever searching for advil at the moment for testing, once it works, then it should search for Prescription Name

class APIPrescription(models.Model):
    def __init__(self, name, warnings  = "", active = "", purpose  = "", usage  = "", generic  = "", dosage  = "", refills  = ""):
        self.name = name
        self.warnings = warnings
        self.active = active
        self.purpose = purpose
        self.usage = usage
        self.generic = generic
        self.dosage = dosage
        self.refills = refills
    
    def __str__(self):
        return self.name

# This is set up as an array because we could have more than 1 prescription and then we would have to search it multiple times or something.
# apiprescriptions = [
#     APIPrescription("advil", data["results"][0]['warnings'],data["results"][0]["active_ingredient"],data['results'][0]['purpose'],data['results'][0]['when_using'],data['results'][0]['openfda']['generic_name'])
# ]

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pets_index(request):
    pets = Pet.objects.filter(user=request.user)
    user_groups = request.user.groups.all()
    print(user_groups)
    vet_pets = Pet.objects.all()
    this_vet = Vet.objects.get(user=request.user)
    this_vet_pets = Pet.objects.filter(vet__id=this_vet.id)

    return render(request, 'pets/index.html', {'pets': pets, 'user_groups': user_groups, 'this_vet_pets':this_vet_pets})

@login_required
def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.checkup_set.all()
    checkup_photos = CheckupPhoto.objects.all()
    apidata = []
    user_groups = request.user.groups.all()
    owner_profile = Profile.objects.get(user= pet.user)
    owner = User.objects.get(id = pet.user_id)
    pet_vet = Vet.objects.get(pet = pet_id)
    for prescription in pet.prescriptions.all():
        url = f'https://api.fda.gov/drug/label.json?api_key={APIKEY}&search={prescription.name}'
        response = requests.get(url)
        data = response.json()
        data_point = APIPrescription(prescription.name,data["results"][0]['warnings'],data["results"][0]["active_ingredient"],data['results'][0]['purpose'],data['results'][0]['when_using'],data['results'][0]['openfda']['generic_name'],prescription.dosage,prescription.refills)
        apidata.append(data_point)
    checkup_form = CheckupForm()
    return render(request, 'pets/detail.html', {'pet': pet, 'apidata': apidata, 'checkup_form': checkup_form, 'checkup_photos': checkup_photos, 'pet_vet':pet_vet, 'user_groups': user_groups, 'owner': owner, 'owner_profile': owner_profile})

# We need to set this up so that only Vets can add pets.
class PetCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.groups.filter(name='vet').exists()
    permission_required = 'main_app.add_pet'
    model = Pet
    fields = ['name', 'type', 'subtype', 'sex', 'birthday', 'color', 'weight']
    success_url = '/pets/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def add_checkup(request, pet_id): 
    form = CheckupForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        new_checkup = form.save(commit=False)
        new_checkup.pet_id = pet_id
        new_checkup.save()

    return redirect('detail', pet_id=pet_id)


class CheckupUpdate(UpdateView):
    model = Checkup
    fields = ['note']

# class CheckupDelete(DeleteView):
#     model = Checkup
#     success_url = '/pets/'

class PetUpdate(UpdateView):
    model = Pet
    fields = ['name', 'type', 'subtype', 'sex', 'birthday', 'color', 'weight']

class PetDelete(DeleteView):
    model = Pet
    success_url = '/pets/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def add_photo(request, pet_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try: 
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      Photo.objects.create(url=url, pet_id=pet_id)
    except:
      print('We have an error here uploading to S3')
  return redirect('detail', pet_id=pet_id)

def add_cuphoto(request, pet_id, checkup_id):
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            CheckupPhoto.objects.create(url=url, checkup_id=checkup_id)
        
        except:
            print('We having an error here uploading to S3')
    return redirect('detail', pet_id=pet_id)
    