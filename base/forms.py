from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Service
from django import forms


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['host', 'participants', 'address']  

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']