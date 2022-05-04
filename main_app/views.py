from django.shortcuts import redirect, render

import uuid
import boto3
from .models import Pet, Photo, CheckupPhoto

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CheckupForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'phtdb'

# Create your views here.



def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pets_index(request):
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'pets/index.html', {'pets': pets})

@login_required
def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    checkup_form = CheckupForm()
    return render(request, 'pets/detail.html', {'pet': pet, 'checkup_form': checkup_form, })

# We need to set this up so that only Vets can add pets.
class PetCreate(LoginRequiredMixin, CreateView):
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

def add_cuphoto(request, checkup_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKEY, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            CheckupPhoto.objects.create(url=url, pet_id=pet_id, checkup_id=checkup_id)
        except:
            print('We having an error here uploading to S3')
    return redirect('detail', pet_id=pet_id)
    