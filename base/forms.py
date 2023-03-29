from django.forms import ModelForm
from .models import Service

class RoomForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'