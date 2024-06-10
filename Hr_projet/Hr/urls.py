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
    path('createEmploye', createEmploye, name="createEmploye"),
]
