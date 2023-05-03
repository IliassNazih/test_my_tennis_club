from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Service
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ServiceForm(ModelForm):
    address = forms.CharField(max_length=255, required=True)
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['host', 'participants']  

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']