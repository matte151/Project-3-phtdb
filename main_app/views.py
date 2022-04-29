from django.shortcuts import redirect, render

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    return render(request, 'base.html')

@login_required
def pet_index(request):
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'pets/index.html', {'pets': pets})


class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['name', 'type', 'subtype', 'sex', 'birthday', 'color', 'weight']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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