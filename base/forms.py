from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Service
from django import forms
#from base.models import Adresse

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['host', 'participants']  

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']