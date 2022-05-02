from django.forms import ModelForm
from .models import Checkup

class CheckupForm(ModelForm):
    class Meta:
        model = Checkup
        field = ['date', 'pet', 'note']