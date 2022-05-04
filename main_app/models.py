import email
from django.db import models
from django.forms import DateField
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)

    def __str__(self):
    	return f"User ID: {self.user} Profile ID: {self.id}"
    

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
    # url = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pet_id': self.id})
    
    def __str__(self):
    	return f"Pet Name: {self.name} ID: {self.id}"


class Checkup(models.Model):
    date = models.DateField()
    note = models.CharField(max_length=200)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('detail', kwargs={'checkup_id': self.id})

    def __str__(self):
	    return f"Date : {self.date} for {self.pet} ID: {self.id}"


class Photo(models.Model):
    url = models.CharField(max_length=200)
    # checkup = models.ForeignKey(Checkup, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
	    return f"Pet : {self.pet} ID: {self.id} URL: {self.url}"   

class CheckupPhoto(models.Model):
    url = models.CharField(max_length=200)
    checkup = models.ForeignKey(Checkup, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
	    return f"Pet : {self.pet} ID: {self.id} URL: {self.url}" 

class Vet(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
	    return f"Vet Name : {self.name} ID: {self.id}"    

# class Prescriptions(models.Model):
#     name = models.CharField(max_length=100)
#     dosage = models.CharField(max_length=50)
#     refills = models.CharField(max_length=100)
#     # api fields needed??????
#     pet = models.ManyToManyField(Pet)
