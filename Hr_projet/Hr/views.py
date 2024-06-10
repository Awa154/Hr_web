from django.shortcuts import render

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
def createEmploye(request):
    return render(request,'admin/employes/create.html')