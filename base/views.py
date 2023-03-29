from django.shortcuts import render, redirect
from .models import Service
from .forms import RoomForm

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


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Service.objects.get(id = pk)
    form = RoomForm(instance= room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance= room)
        if form.is_valid():
            form.save()
            return redirect()
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
