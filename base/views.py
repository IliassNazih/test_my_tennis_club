from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Service, Topic, Message
from .forms import ServiceForm

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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

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

def userProfile(request):
    context{}
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