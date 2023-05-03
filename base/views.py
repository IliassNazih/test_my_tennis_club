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
#from base.models import Adresse

# services = [
#     {'id':1, 'name':'deneigement'},
#     {'id':2, 'name':'tondeuse'},
#     {'id':3, 'name':'laveauto'},
# ]

def loginPage(request):
    
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
    logout(request)
    return redirect('home')

def registerPage(request):
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
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request,'base/profile.html', context)
    

@login_required(login_url = 'login')
def createService(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit= False)
            service.host = request.user
            service.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/service_form.html', context)

@login_required(login_url = 'login')
def updateService(request, pk):
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
    service = Service.objects.get(id=pk)

    if request.user != service.host:
        return HttpResponse('You are not allowed to delete this service')


    if request.method == 'POST':
        service.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': service})

def map_view(request):
    map = folium.Map(location=[45.53832923645949, -73.67523042389348], zoom_start=13)

    # Add a marker to the map
    folium.Marker([45.53832923645949, -73.67523042389348], popup='Montreal,QC').add_to(map)
    


    map_html = map._repr_html_()
    context = {'map_html': map_html}
    return render(request, 'map.html', context)

#def liste_adresses(request):
    adresses = Adresse.objects.all()
    return render(request, 'liste_adresses.html', {'adresses': adresses})