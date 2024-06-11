from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login', login, name="login"),
    path('services', services, name="services"),
    path('annonces', annonces, name="annonces"),
    path('about', about, name="about"),
    path('adminPage', admin, name="adminPage"),
    path('adminPage', admin, name="adminPage"),
    path('createCompte', createCompte, name="createCompte"),
    path('editEmploye', editEmploye, name="editEmploye"),
    path('listeEmploye', listeEmploye, name="listeEmploye"),
    path('editEntreprise', editEntreprise, name="editEntreprise"),
    path('listeEntreprise', listeEntreprise, name="listeEntreprise"),
]
