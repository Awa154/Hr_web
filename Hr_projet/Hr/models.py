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
    email=models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    adresse=models.CharField(max_length=50)
    contact=PhoneNumberField(unique=True)
    ville = models.CharField(max_length=100, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    role=models.CharField(max_length=2, choices=ROLE_CHOICES)
    photo_profile = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Champ pour indiquer si le compte est actif
    
    
class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    departement=models.CharField(max_length=25)
    poste_occupe=models.CharField(max_length=25)
    
class EmailSettings(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=587)
    host_user = models.CharField(max_length=255)
    host_password = models.CharField(max_length=255)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)

    def __str__(self):
        return f"Email Settings: {self.host}"
     
class Competence(models.Model):
    nom = models.CharField(max_length=100)

class Employe(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    domaine=models.CharField(max_length=25)
    departement=models.CharField(max_length=25)
    competences = models.ManyToManyField(Competence)
    annee_exp=models.IntegerField()
    
    
class Entreprise(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/')
    nom_entreprise = models.CharField(max_length=255)
    site_web = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    