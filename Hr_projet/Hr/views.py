import re

from django.conf import settings
from django.http import JsonResponse
from Hr_projet.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Competence, Contrat, DemandeEmploye, EmailSettings, Utilisateurs, Employe, Entreprise, Administrateur
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

#Fonction pour retourner la vue vers la page d'accueil
def home(request):
    return render(request,'home/home.html', {'active_page': 'home'})

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
def adminPage(request):
    # Récupérer tous les utilisateurs
    users = Utilisateurs.objects.all()

    # Statistiques
    total_users = users.count()
    total_employees = users.filter(role="EM").count()
    total_partners = users.filter(role="EN").count()

    context = {
        'total_users': total_users,
        'total_employees': total_employees,
        'total_partners': total_partners
    }
    return render(request,'admin/admin.html', context)

#Fonction pour activé ou désactivé un utilisateur
def status(request, user_id):
    user = Utilisateurs.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"Le statut de {user.email} a été mis à jour.")
    return redirect('adminPage')

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
        
        # Vérifier les règles de mot de passe (sans caractère spécial)
        if password and not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins une lettre minuscule, une lettre majuscule, un chiffre et être composé d'au moins 8 caractères.")
            
        # Vérifier l'unicité de l'email et du contact
        if Utilisateurs.objects.filter(email=email).exists():
            errors.append("Un utilisateur avec cet email existe déjà.")
        if Utilisateurs.objects.filter(contact=contact).exists():
            errors.append("Un utilisateur avec ce contact existe déjà.")

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
            role=role,
            password=make_password(password)
        )
        user.save()
        
        # Envoyer l'email avec les identifiants de connexion
        subject = "Votre compte a été créé"
        message = f"Bonjour {prenom} {nom},\n\nVotre compte a été créé avec succès.\n\nVoici vos identifiants de connexion :\nEmail : {email}\nMot de passe : {password}\n\nMerci de vous connecter et de changer votre mot de passe dès que possible."
        from_email = EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Compte créé avec succès! Un email avec les identifiants de connexion de l'utilisateur a été envoyé.")
        except Exception as e:
            messages.error(request, f"Le compte a été créé, mais l'email n'a pas pu être envoyé : {e}")

        # Créer le modèle associé basé sur le rôle de l'utilisateur
        if role == "EM":
            domaine = request.POST.get('domaine')
            departement = request.POST.get('departement')
            annee_exp = request.POST.get('annee_exp')
            employe = Employe.objects.create(
                utilisateur=user,
                departement=departement,
                domaine=domaine,
                annee_exp=annee_exp
            )
            # Récupérer les compétences du formulaire
            competences = request.POST.getlist('competences')
            # Parcourir chaque compétence et la sauvegarder dans la base de données
            for competence in competences:
                Competence.objects.create(employe=employe, competence=competence)
                    
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
            
        return redirect('createCompte')  # Redirige vers la page d'inscription ou une autre page de votre choix
    return render(request, "admin/comptes/create.html")

#Fonction pour retourner la vue vers la page de la liste comptes
def listeCompte(request):
    # Récupérer tous les utilisateurs
    users = Utilisateurs.objects.all()

    # Statistiques
    total_users = users.count()
    total_employees = users.filter(role="EM").count()
    total_partners = users.filter(role="EN").count()

    # Recherche
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(nom__icontains=query)|
            Q(prenom__icontains=query)|
            Q(email__icontains=query)|
            Q(contact__icontains=query)|
            Q(adresse__icontains=query)|
            Q(ville__icontains=query) |
            Q(pays__icontains=query) |
            Q(role__icontains=query)
           )

    context = {
        'users': users,
        'total_users': total_users,
        'total_employees': total_employees,
        'total_partners': total_partners
    }
    return render(request,"admin/comptes/liste.html", context )

#Fonction pour retourner la vue vers la page d'accueil
def homeEmploye(request):
    return render(request,'home/employes/home.html',{'active_page': 'homeEmploye'} )

#Fonction pour retourner la vue vers la page de la liste des employes
def listeEmploye(request):
    employes = Employe.objects.select_related('utilisateur').prefetch_related('competence_set').all()
      
    # Recherche
    query = request.GET.get('q')
    if query:
        employes = employes.filter(
            Q(utilisateur__nom__icontains=query)|
            Q(utilisateur__prenom__icontains=query)|
            Q(domaine__icontains=query)|
            Q(competence_set__competence__icontains=query)
           )

    context = {
        'employes': employes,
    }
    return render(request,'admin/comptes/listeEmploye.html', context)

#Fonction pour retourner la vue vers la page d'accueil
def homeEntreprise(request):
    return render(request,'home/employes/home.html', {'active_page': 'homeEntreprise'})

#Fonction pour retourner la vue vers la page de la liste des entreprises
def listeEntreprise(request):
    entreprises = Entreprise.objects.select_related('utilisateur').all()
      
    # Recherche
    query = request.GET.get('q')
    if query:
        entreprises = entreprises.filter(
            Q(utilisateur__nom_entreprise__icontains=query)|
            Q(utilisateur__nom__icontains=query)|
            Q(utilisateur__prenom__icontains=query)
           )

    context = {
        'entreprises': entreprises,
    }
    return render(request,'admin/comptes/listeEntreprise.html',context)

#Fonction pour retourner la vue vers la page de login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Récupérer l'utilisateur avec l'email donné
        try:
            user = Utilisateurs.objects.get(email=email)
            
            if not user.is_active:
                messages.error(request, "Votre compte est désactivé.")
                return render(request, "auth/login.html")
            
            if check_password(password, user.password):
                # Créer une session pour l'utilisateur
                request.session['user_id'] = user.id
                # Redirection basée sur le rôle
                if user.role == "AD":
                    return redirect('adminPage')  # Rediriger vers la page d'administration
                elif user.role == "EM":
                    return redirect('homeEmploye')  # Rediriger vers la page employé
                elif user.role == "EN":
                    return redirect('homeEntreprise')  # Rediriger vers la page entreprise
                messages.success(request, "Vous êtes maintenant connecter!")
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
        except Utilisateurs.DoesNotExist:
            messages.error(request, "Email ou mot de passe inexistent.")

    return render(request, "auth/login.html")

#Fonction de déconnexion
def logout(request):
    # Supprimez la session de l'utilisateur
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('home')

#Fonction pour changer le mot de passe en cas d'oublie
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = Utilisateurs.objects.get(email=email)
            temp_password = temp_pass()
            user.password = make_password(temp_password)
            user.save()

            send_mail(
                'Votre mot de passe temporaire',
                f'Votre nouveau mot de passe temporaire est : {temp_password}\nVeuillez le changer après vous être connecté.',
                EMAIL_HOST_USER,
                [email],
                fail_silently=True,
            )

            messages.success(request, "Un mot de passe temporaire vous a été envoyé par email.")
            return redirect('login')
        except Utilisateurs.DoesNotExist:
            messages.error(request, "Aucun utilisateur trouvé avec cet email.")
            
    return render(request, "auth/forgot_password.html")

#Fonction pour générer un mot de passe temporaire le temps que l'utilisateur le change lui même
def temp_pass(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

#Fonction pour modifier son mot de passe
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not check_password(current_password, user.password):
            messages.error(request, "Le mot de passe actuel est incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Mot de passe changé avec succès.")
            if user.role == "AD":
                return redirect('profile_admin')
            elif user.role == "EM":
                return redirect('profile_employe')
            elif user.role == "EN":
                return redirect('profile_entreprise')

    return render(request, 'auth/change_password.html')


#Fonction pour mettre à jour le profile d'un employe
def profile_employe(request):
    if not request.user or not hasattr(request.user, 'id'):
        messages.error(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('login')
    user = request.user
    
    # Récupérer les informations administratives
    try:
        employe_info = Employe.objects.get(utilisateur=user)
    except Employe.DoesNotExist:
        messages.error(request, "Les informations de votre compte n'ont pas été trouvées.")
        return redirect('homeEmploye')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        contact = request.POST.get('contact')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        photo_profile = request.FILES.get('photo_profile')
        domaine = request.POST.get('domaine')
        departement = request.POST.get('departement')
        competence = request.POST.get('competence')
        annee_exp = request.POST.get('annee_exp')

        # Validation de l'email et du contact unique
        if Utilisateurs.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
        elif Utilisateurs.objects.filter(contact=contact).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec ce contact existe déjà.")
        else:
            user.nom = nom
            user.prenom = prenom
            user.email = email
            user.adresse = adresse
            user.contact = contact
            user.ville = ville
            user.pays = pays
            if photo_profile:
                user.photo_profile = photo_profile
            user.save()

            employe_info.domaine = domaine
            employe_info.departement = departement
            employe_info.competence = competence
            employe_info.annee_exp = annee_exp
            employe_info.save()

            messages.success(request, "Profil employé mis à jour avec succès.")
            return redirect('profile_employe')
    return render(request, 'home/employes/profile.html', {'user': user, 'employe_info': employe_info})

#Fonction pour accéder au profile utilisateur d'une entreprise
def profile_entreprise(request):
    if not request.user or not hasattr(request.user, 'id'):
        messages.error(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('login')
    user = request.user
    
    # Récupérer les informations administratives
    try:
        entreprise_info = Entreprise.objects.get(utilisateur=user)
    except Entreprise.DoesNotExist:
        messages.error(request, "Les informations de votre compte n'ont pas été trouvées.")
        return redirect('homeEntreprise')
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        contact = request.POST.get('contact')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        photo_profile = request.FILES.get('photo_profile')
        nom_entreprise = request.POST.get('nom_entreprise')
        description = request.POST.get('description')
        site_web = request.POST.get('site_web')
        logo = request.FILES.get('logo')

        # Validation de l'email et du contact unique
        if Utilisateurs.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
        elif Utilisateurs.objects.filter(contact=contact).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec ce contact existe déjà.")
        else:
            user.nom = nom
            user.prenom = prenom
            user.email = email
            user.adresse = adresse
            user.contact = contact
            user.ville = ville
            user.pays = pays
            if photo_profile:
                user.photo_profile = photo_profile
            user.save()

            entreprise_info.nom_entreprise = nom_entreprise
            entreprise_info.description = description
            entreprise_info.site_web = site_web
            if logo:
                entreprise_info.logo = logo
            entreprise_info.save()

            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('homeEntreprise')
    return render(request, 'home/entreprises/profile.html', {'user': user, 'entreprise_info': entreprise_info})

#Fonction pour retourner le profile administrateur
def profile_admin(request):
    if not request.user or not hasattr(request.user, 'id'):
        messages.error(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('login')

    user = request.user

    # S'assurer que l'utilisateur est un administrateur
    if user.role != "AD":
        messages.error(request, "Vous n'avez pas les droits d'accès à cette page.")
        return redirect('adminPage')

    # Récupérer les informations administratives
    try:
        admin_info = Administrateur.objects.get(utilisateur=user)
    except Administrateur.DoesNotExist:
        messages.error(request, "Les informations administratives n'ont pas été trouvées.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        contact = request.POST.get('contact')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        photo_profile = request.FILES.get('photo_profile')
        departement = request.POST.get('departement')
        poste_occupe = request.POST.get('poste_occupe')

        # Validation de l'email et du contact unique
        if Utilisateurs.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
        elif Utilisateurs.objects.filter(contact=contact).exclude(id=user.id).exists():
            messages.error(request, "Un utilisateur avec ce contact existe déjà.")
        else:
            user.nom = nom
            user.prenom = prenom
            user.email = email
            user.adresse = adresse
            user.contact = contact
            user.ville = ville
            user.pays = pays
            if photo_profile:
                user.photo_profile = photo_profile
            user.save()

            admin_info.departement = departement
            admin_info.poste_occupe = poste_occupe
            admin_info.save()

            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('adminPage')

    return render(request, 'admin/profile.html', {'user': user, 'admin_info': admin_info})


#Fonction pour la création d'un contrat
def createContrat(request):
    if request.method == "POST":
        employe_id = request.POST.get('employe')
        entreprise_id = request.POST.get('entreprise')
        
        employe = Employe.objects.get(id=employe_id)
        entreprise = Entreprise.objects.get(id=entreprise_id)
        
        contrat = Contrat(
            employe=employe,
            entreprise=entreprise,
            date_debut=request.POST.get('date_debut'),
            date_fin=request.POST.get('date_fin'),
            type_contrat=request.POST.get('type_contrat'),
            nom_entreprise_employeur=entreprise.nom_entreprise,
            contact_entreprise=entreprise.utilisateur.contact,
            email_entreprise=entreprise.utilisateur.email,
            adresse_entreprise=entreprise.utilisateur.adresse,
            nom_employe=employe.utilisateur.nom,
            prenom_employe=employe.utilisateur.prenom,
            contact_employe=employe.utilisateur.contact,
            email_employe=employe.utilisateur.email,
            adresse_employe=employe.utilisateur.adresse,
            type_remuneration=request.POST.get('type_remuneration'),
            montant=request.POST.get('montant'),
            status=True
        )
        contrat.save()
        return redirect('listeContrat',{'employes': employes, 'entreprises': entreprises})  # Rediriger vers une page de liste des contrats après l'enregistrement
    
    employes = Employe.objects.all()
    entreprises = Entreprise.objects.all()
    return render(request,'admin/contrats/create.html',{'employes': employes, 'entreprises': entreprises})

#Fonction pour récupérer les informations sélectionnés pour établir le contrat et remplir directement les champs concernés
def get_employe_details(request, employe_id):
    employe = Employe.objects.get(id=employe_id)
    data = {
        'nom': employe.utilisateur.nom,
        'prenom': employe.utilisateur.prenom,
        'contact': str(employe.utilisateur.contact),
        'email': employe.utilisateur.email,
        'adresse': employe.utilisateur.adresse,
    }
    return JsonResponse(data)

#Fonction pour récupérer les informations sélectionnés pour établir le contrat et remplir directement les champs concernés
def get_entreprise_details(request, entreprise_id):
    entreprise = Entreprise.objects.get(id=entreprise_id)
    data = {
        'nom_entreprise': entreprise.nom_entreprise,
        'contact': str(entreprise.utilisateur.contact),
        'email': entreprise.utilisateur.email,
        'adresse': entreprise.utilisateur.adresse,
    }
    return JsonResponse(data)

#Fonction pour afficher la liste des contrats
def listeContrat(request):
    statut_filtre = request.GET.get('statut', 'tous')
    
    if statut_filtre == 'actif':
        contrats = Contrat.objects.filter(status=True)
    elif statut_filtre == 'inactif':
        contrats = Contrat.objects.filter(status=False)
    else:
        contrats = Contrat.objects.all()
    return render(request,'admin/contrats/liste.html',{'contrats': contrats, 'statut_filtre': statut_filtre})

#Fonction pour faire une demande d'employé de la part d'une entreprise
def creer_demande(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'entreprise'):
        return redirect('login')  # Rediriger vers la page de login si l'utilisateur n'est pas connecté ou n'est pas une entreprise
    
    entreprise = request.user.entreprise  # Récupérer l'entreprise associée à l'utilisateur connecté
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        details = request.POST.get('details')
        competences_recherchees = request.POST.get('competences_recherchees')
        
        demande = DemandeEmploye(
            entreprise=entreprise,
            titre=titre,
            details=details,
            competences_recherchees=competences_recherchees,
        )
        demande.save()
        
        return redirect('demande_confirmee')  # Rediriger vers une page de confirmation

    return render(request, 'creer_demande.html', {'entreprise': entreprise})

#Fonction pour envoyer les notifications à l'entreprise qui à fait la demande dans les différents cas
def envoyer_notification(self):
    recipient_list= EMAIL_HOST_USER
    from_email = [self.entreprise.utilisateur.email]
    if self.statut == 'VALIDÉ':
        message = f"Votre demande '{self.titre}' a été validée. Un employé correspondant à été sélectionné et si vous êtes satisfait, nous pourrons vous établir votre contrat avec cet employé"
    elif self.statut == 'EN_ATTENTE':
        message = f"Votre demande '{self.titre}' est en cours de traitement."
    elif self.statut == 'REFUSÉ':
        message = f"Nous n'avons trouvé aucun employé correspondant à votre demande '{self.titre}'."
    
    send_mail(
        'Statut de votre demande d\'employé',
        message,
        recipient_list,
        from_email,
        fail_silently=False,
    )
    
    
def configurer_email(request):
    email_settings, created = EmailSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        email_settings.host = request.POST.get('host')
        email_settings.port = request.POST.get('port')
        email_settings.host_user = request.POST.get('host_user')
        email_settings.host_password = request.POST.get('host_password')
        email_settings.use_tls = 'use_tls' in request.POST
        email_settings.use_ssl = 'use_ssl' in request.POST
        email_settings.save()

        # Mettre à jour les settings dynamiquement
        settings.EMAIL_HOST = email_settings.host
        settings.EMAIL_PORT = email_settings.port
        settings.EMAIL_HOST_USER = email_settings.host_user
        settings.EMAIL_HOST_PASSWORD = email_settings.host_password
        settings.EMAIL_USE_TLS = email_settings.use_tls
        settings.EMAIL_USE_SSL = email_settings.use_ssl

        return redirect('configurer_email')

    return render(request, 'configurer_email.html', {'email_settings': email_settings})
    
    