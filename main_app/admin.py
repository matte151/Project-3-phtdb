from django.contrib import admin

# Register your models here.
from .models import CheckupPhoto, Pet, Checkup, Photo, Prescription, Vet, Profile

admin.site.register(Pet)
admin.site.register(Checkup)
admin.site.register(Photo)
admin.site.register(Vet)
admin.site.register(Profile)
admin.site.register(Prescription)
admin.site.register(CheckupPhoto)