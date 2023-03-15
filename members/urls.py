from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.Member, name = 'members'),
]