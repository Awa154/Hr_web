import re
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Utilisateurs, Employe, Entreprise, Administrateur

# Create your views here.

#Fonction pour retourner la vue vers la page d'accueil
def home(request):
    return render(request,'home/home.html', {'active_page': 'home'})

#Fonction pour retourner la vue vers la page de connexin
def login(request):
    return render(request,'auth/login.html')

#Fonction pour retourner la vue vers la page des différents services offerts par l'agence
def services(request):
    return render(request,'home/services.html', {'active_page': 'services'})

#Fonction pour retourner la vue vers la page des différentes annonces 
def annonces(request):
    return render(request,'home/annonces.html', {'active_page': 'annonces'})

#Fonction pour retourner la vue vers la page de renseignement
def about(request):
    return render(request,'home/about.html', {'active_page': 'about'})

#Fonction pour retourner la vue vers la page de l'administrateur
def admin(request):
    return render(request,'admin/admin.html')

#Fonction pour retourner la vue vers la page de création de compte
def createCompte(request):
    if request.method == "POST":
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        contact = request.POST.get('contact')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        # Valider les données
        errors = []
        if not nom:
            errors.append("Le nom est requis.")
        if not prenom:
            errors.append("Le prénom est requis.")
        if not email:
            errors.append("L'email est requis.")
        if not adresse:
            errors.append("L'adresse est requise.")
        if not contact:
            errors.append("Le contact est requis.")
        if not role:
            errors.append("Le rôle est requis.")
        if not password:
            errors.append("Le mot de passe est requis.")
        if password != password_confirmation:
            errors.append("Les mots de passe ne correspondent pas.")
        
        # Vérifier les règles de mot de passe
        if password and not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$&])[A-Za-z\d@$&]{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.")

        # Afficher les erreurs
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('createCompte')
        
        # Créer l'utilisateur
        user = Utilisateurs(
            nom=nom,
            prenom=prenom,
            email=email,
            adresse=adresse,
            contact=contact,
            ville=ville,
            pays=pays,
            password=make_password(password)
        )
        user.save()

        # Créer le modèle associé basé sur le rôle de l'utilisateur
        if role == "EM":
            domaine = request.POST.get('domaine')
            departement = request.POST.get('departement')
            competence = request.POST.get('competence')
            annee_exp = request.POST.get('annee_exp')
            Employe.objects.create(
                utilisateur=user,
                departement=departement,
                domaine=domaine,
                competence=competence,
                annee_exp=annee_exp
            )
        elif role == "EN":
            nom_entreprise = request.POST.get('nom_entreprise')
            description = request.POST.get('description')
            site_web = request.POST.get('site_web')
            logo = request.FILES.get('logo')
            Entreprise.objects.create(
                utilisateur=user,
                nom_entreprise=nom_entreprise,
                description=description,
                site_web=site_web,
                logo=logo
            )
        elif role == "AD":
            departement = request.POST.get('departement')
            poste_occupe = request.POST.get('poste_occupe')
            Administrateur.objects.create(
                utilisateur=user,
                departement=departement,
                poste_occupe=poste_occupe
            )
            
            # Ajouter le message de succès avant la redirection
        messages.success(request, "Compte créé avec succès!")
        return redirect('createCompte')  # Redirige vers la page d'inscription ou une autre page de votre choix
    return render(request, "admin/comptes/create.html")

#Fonction pour retourner la vue vers la page de la mise à jour du profil d'un employe
def editEmploye(request):
    return render(request,'admin/employes/edit.html')

#Fonction pour retourner la vue vers la page de la mise à jour du profil d'une entreprise
def editEntreprise(request):
    return render(request,'admin/entrepises/edit.html')


#Fonction pour retourner la vue vers la page de la liste des employes
def listeEmploye(request):
    return render(request,'admin/employes/liste.html')

#Fonction pour retourner la vue vers la page de la liste des entreprises
def listeEntreprise(request):
    return render(request,'admin/entreprises/liste.html')