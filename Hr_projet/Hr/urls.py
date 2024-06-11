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
    path('homeEmploye', homeEmploye, name="homeEmploye"),
    path('editEmploye', editEmploye, name="editEmploye"),
    path('listeEmploye', listeEmploye, name="listeEmploye"),
    path('homeEntreprise',homeEntreprise, name="homeEntreprise"),
    path('editEntreprise', editEntreprise, name="editEntreprise"),
    path('listeEntreprise', listeEntreprise, name="listeEntreprise"),
]
