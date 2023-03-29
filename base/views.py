from django.shortcuts import render
from .models import Service

# rooms = [
#     {'id':1, 'name':'deneigement'},
#     {'id':2, 'name':'tondeuse'},
#     {'id':3, 'name':'laveauto'},
# ]

def home(request):
    rooms = Service.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Service.objects.get(id=pk)   
    context = {'room': room}
    return render(request, 'base/room.html', context)

