from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Service, Topic, Message
from .forms import ServiceForm,SignUpForm
from geopy.geocoders import Nominatim
import folium


def loginPage(request):
    """
    Cette méthode gère la page de connexion.
    -Si l'utilisateur est déjà authentifié, il est redirigé vers la page d'accueil.
    -Si la méthode de requête est POST, elle récupère les informations de connexion (nom d'utilisateur et mot de passe) à partir de la requête.
    -Elle tente de trouver un utilisateur correspondant au nom d'utilisateur fourni.
    -Si l'utilisateur existe, elle utilise la fonction authenticate pour vérifier les informations de connexion.
    -Si les informations de connexion sont valides, l'utilisateur est connecté et redirigé vers la page d'accueil.
    -Sinon, un message d'erreur est affiché.
    -Si la méthode de requête est GET, elle affiche la page de connexion.
    -La variable de contexte page est utilisée pour spécifier le contexte de la page.
    -La méthode renvoie le rendu du modèle login_register.html avec le contexte.
    """
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    """
    Cette méthode gère la déconnexion de l'utilisateur.
    -Elle utilise la fonction logout pour déconnecter l'utilisateur.
    -Ensuite, l'utilisateur est redirigé vers la page d'accueil.
    """
    logout(request)
    return redirect('home')

def infos(request):
    """
    Cette méthode gère la page d'informations.
    -Elle utilise le modèle infos.html pour afficher les informations
    """
    context = {'infos': infos}
    return render(request, 'base/infos.html', context)

def messagerie(request,pk):
    """
    Cette méthode gère la messagerie pour un service spécifique.
    -Elle récupère le service correspondant à l'ID fourni (pk).
    -Elle récupère toutes les conversations liées à ce service, triées par date de création.
    -Si la méthode de requête est POST, elle crée un nouveau message à partir des informations fournies dans la requête (corps du message, utilisateur et service associés).
    -Ensuite, l'utilisateur est redirigé vers la page de messagerie pour le service.
    -La méthode renvoie le rendu du modèle messagerie.html avec le contexte.
    """
    service = Service.objects.get(id=pk)
    conversation = service.message_set.all().order_by('created')
    if request.method == 'POST':
        message = Message.objects.create(user= request.user,
                                         service = service,
                                         body = request.POST.get('body'))
        return redirect('message', pk = service.id)
    context = {'service': service, 'conversation': conversation}
    return render(request, 'base/messagerie.html', context)

def registerPage(request):
    """
    Cette méthode gère la page d'inscription.
    -Si la méthode de requête est POST, elle crée un formulaire d'inscription avec les données de la requête.
    -Si le formulaire est valide, un nouvel utilisateur est enregistré et connecté.
    -Ensuite, l'utilisateur est redirigé vers la page d'accueil.
    -Si la méthode de requête est GET, elle affiche le formulaire d'inscription.
    -La méthode renvoie le rendu du modèle login_register.html avec le formulaire dans le contexte.
    """
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    """
    Cette méthode gère la page d'accueil.
    -Elle permet de rechercher des services en fonction d'un terme de recherche (q).
    -Elle filtre les services en fonction du terme de recherche dans les champs 'topic', 'name' et 'description'.
    -Elle récupère tous les sujets et compte le nombre total de services.
    -La méthode renvoie le rendu du modèle home.html avec les services, les sujets et le nombre de services dans le contexte.
    """
    q=request.GET.get('q') if request.GET.get('q') !=None else ''

    services = Service.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    service_count = services.count()

    context = {'services':services, 'topics':topics, 'service_count':service_count}
    return render(request, 'base/home.html', context)

def service(request, pk):
    """
    Cette méthode gère la page d'un service spécifique.
    -Elle récupère le service correspondant à l'ID fourni (pk).
    -Elle récupère tous les messages liés à ce service, triés par date de création (du plus récent au plus ancien).
    -Si la méthode de requête est POST, elle crée un nouveau message à partir des informations fournies dans la requête (corps du message, utilisateur et service associés).
    -Ensuite, l'utilisateur est redirigé vers la page du service.
    -La méthode renvoie le rendu du modèle service.html avec le service et les messages dans le contexte.
    """
    service = Service.objects.get(id=pk)
    service_messages = service.message_set.all().order_by('-created')

    if request.method == 'POST':
        message = Message.objects.create(user= request.user,
                                         service = service,
                                         body = request.POST.get('body'))
        return redirect('service', pk = service.id)

    context = {'service': service, 'service_messages': service_messages}
    return render(request, 'base/service.html', context)


def userProfile(request, pk):
    """
    Cette méthode gère le profil d'un utilisateur spécifique.
    -Elle récupère l'utilisateur correspondant à l'ID fourni (pk).
    -Elle permet de rechercher des services en fonction d'un terme de recherche (q).
    -Elle filtre les services en fonction du terme de recherche dans les champs 'topic', 'name' et 'description'.
    -La méthode renvoie le rendu du modèle profile.html avec l'utilisateur et les services dans le contexte.
    """
    user = User.objects.get(id=pk)
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    services = Service.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    context = {'user': user, 'services':services}
    return render(request,'base/profile.html', context)
    

@login_required(login_url = 'login')
def createService(request):
    """
    Cette méthode gère la création d'un nouveau service.
    -Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion.
    -Si la méthode de requête est POST, elle crée un formulaire de service avec les données de la requête.
    -Si le formulaire est valide, le service est enregistré avec l'utilisateur actuel comme hôte.
    -Ensuite, l'utilisateur est redirigé vers la page d'accueil.
    -Si la méthode de requête est GET, elle affiche le formulaire de service.
    -La méthode renvoie le rendu du modèle service_form.html avec le formulaire dans le contexte.
    """
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit= False)
            service.host = request.user
            service.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/service_form.html', context)

@login_required(login_url = 'login')
def updateService(request, pk):
    """
    Cette méthode gère la mise à jour d'un service existant.
    -Elle récupère le service correspondant à l'ID fourni (pk).
    -Si l'utilisateur n'est pas l'hôte du service, un message d'erreur est affiché.
    -Si la méthode de requête est POST, elle crée un formulaire de service avec les données de la requête et l'instance du service existant.
    -Si le formulaire est valide, le service est mis à jour.
    -Ensuite, l'utilisateur est redirigé vers la page d'accueil.
    -La méthode renvoie le rendu du modèle service_form.html avec le formulaire dans le contexte.
    """
    service = Service.objects.get(id = pk)
    form = ServiceForm(instance= service)

    if request.user != service.host:
        return HttpResponse('You are not allowed to update this service')

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance = service)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/service_form.html', context)

@login_required(login_url = 'login')
def deleteService(request, pk):
    """
    Cette méthode gère la suppression d'un service existant.
    -Elle récupère le service correspondant à l'ID fourni (pk).
    -Si l'utilisateur n'est pas l'hôte du service, un message d'erreur est affiché.
    -Si la méthode de requête est POST, le service est supprimé de la base de données.
    -Ensuite, l'utilisateur est redirigé vers la page d'accueil.
    -Si la méthode de requête est GET, elle affiche la page de confirmation de suppression.
    -La méthode renvoie le rendu du modèle delete.html avec le service dans le contexte.
    """
    service = Service.objects.get(id=pk)

    if request.user != service.host:
        return HttpResponse('You are not allowed to delete this service')


    if request.method == 'POST':
        service.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': service})

def map_view(request):
    """
    Cette méthode affiche une carte avec des marqueurs pour chaque service.
    -Elle utilise le module geopy pour géocoder les adresses des services.
    -Elle utilise le module folium pour générer la carte avec les marqueurs.
    -La méthode renvoie le rendu du modèle map.html avec le code HTML de la carte dans le contexte.
"""
    geolocator = Nominatim(user_agent="TEST_MY_TENNIS_CLUB")
    bdeb = geolocator.geocode('10555 Ave de Bois-de-Boulogne, Montreal')
    map = folium.Map(location=[bdeb.latitude, bdeb.longitude], zoom_start=10)

    for obj in Service.objects.all():
        location = geolocator.geocode(obj.address)
        if location is not None:
            latitude = location.latitude
            longitude = location.longitude
            popup_text = f"<b>{obj.topic}</b><br>{obj.name}"
        folium.Marker([latitude, longitude], popup=popup_text).add_to(map)

    map_html = map._repr_html_()
    context = {'map_html': map_html}
    return render(request, 'map.html', context)

def service_map_view(request, pk):
    """
    Cette méthode affiche une carte avec un marqueur pour un service spécifique.
    -Elle récupère le service correspondant à l'ID fourni (pk).
    -Elle utilise le module geopy pour géocoder l'adresse du service.
    -Elle utilise le module folium pour générer la carte avec le marqueur.
    -La méthode renvoie le rendu du modèle map_service.html avec le code HTML de la carte dans le contexte.
    """
    
    service = Service.objects.get(id=pk)

    
    geolocator = Nominatim(user_agent="TEST_MY_TENNIS_CLUB")

    
    location = geolocator.geocode(service.address)

    
    maps = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)

    
    popup_text = f"<b>{service.topic}</b><br>{service.name}"
    folium.Marker([location.latitude, location.longitude], popup=popup_text).add_to(maps)

    
    map_service_html = maps._repr_html_()

    
    context = {'map_service_html': map_service_html}

    return render(request, 'map_service.html', context)