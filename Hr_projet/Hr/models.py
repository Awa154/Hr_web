from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Utilisateurs(models.Model):
    #Définition des différents types de role d'un utilisateur
    ROLE_CHOICES = [
        ("AD", "Admin"),
        ("EM", "Employe"),
        ("EN", "Entreprise"),
    ]
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=150)
    email=models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    adresse=models.CharField(max_length=50)
    contact=PhoneNumberField()
    ville = models.CharField(max_length=100, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    role=models.CharField(max_length=2, choices=ROLE_CHOICES)
    
    
class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    departement=models.CharField(max_length=25)
    poste_occupe=models.CharField(max_length=25)
    
    
class Employe(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    domaine=models.CharField(max_length=25)
    departement=models.CharField(max_length=25)
    competence=models.CharField(max_length=25)
    annee_exp=models.IntegerField()
    
    
class Entreprise(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/')
    nom_entreprise = models.CharField(max_length=255)
    site_web = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    