from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Service, Topic
from .forms import ServiceForm

# services = [
#     {'id':1, 'name':'deneigement'},
#     {'id':2, 'name':'tondeuse'},
#     {'id':3, 'name':'laveauto'},
# ]

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
    context = {'service': service}
    return render(request, 'base/service.html', context)


def createService(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/service_form.html', context)

def updateService(request, pk):
    service = Service.objects.get(id = pk)
    form = ServiceForm(instance= service)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance = service)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/service_form.html', context)

def deleteService(request, pk):
    service = Service.objects.get(id=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': service})