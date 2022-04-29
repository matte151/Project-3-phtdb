import email
from django.db import models
# from django.forms import DateField
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    subtype = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    birthday = models.DateField()
    color = models.CharField(max_length=100)
    weight = models.IntegerField()
    notes = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Checkup(models.Model):
    date = models.DateField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    checkup = models.ForeignKey(Checkup, on_delete=models.CASCADE)

class Vet(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=50)
    phone = models.PhoneNumberField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

# class Prescriptions(models.Model):
#     name = models.CharField(max_length=100)
#     dosage = models.CharField(max_length=50)
#     refills = models.CharField(max_length=100)
#     api fields needed??????
#     pet = models.ManyToManyField(Pet)
