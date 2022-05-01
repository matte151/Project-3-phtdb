from django.contrib import admin

# Register your models here.
from .models import Pet, Checkup, Photo, Vet, Profile

admin.site.register(Pet)
admin.site.register(Checkup)
admin.site.register(Photo)
admin.site.register(Vet)
admin.site.register(Profile)