from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('change_password', change_password, name='change_password'),
    path('services', services, name="services"),
    path('annonces', annonces, name="annonces"),
    path('about', about, name="about"),
    path('adminPage', adminPage, name="adminPage"),
    path('profile_admin', profile_admin, name="profile_admin"),
    path('status/<int:user_id>/', status, name='status'),
    path('createCompte', createCompte, name="createCompte"),
    path('homeEmploye', homeEmploye, name="homeEmploye"),
    path('profile_employe', profile_employe, name="profile_employe"),
    path('listeEmploye', listeEmploye, name="listeEmploye"),
    path('homeEntreprise',homeEntreprise, name="homeEntreprise"),
    path('profile_entreprise', profile_entreprise, name="profile_entreprise"),
    path('listeEntreprise', listeEntreprise, name="listeEntreprise"),
    path('dash', dash, name="dash"),
]
