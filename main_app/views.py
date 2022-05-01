from django.shortcuts import redirect, render

from .models import Pet

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pets_index(request):
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'pets/index.html', {'pets': pets})


def pets_detail(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    return render(request, 'pets/detail.html', {'pet': pet })

# We need to set this up so that only Vets can add pets.
class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['name', 'type', 'subtype', 'sex', 'birthday', 'color', 'weight']
    success_url = '/pets/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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