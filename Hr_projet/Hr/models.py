from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Utilisateurs(models.Model):
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=150)
    email=models.EmailField(max_length=200)
    adresse=models.CharField(max_length=50)
    contact=models.PhoneNumberField()