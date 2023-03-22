from django.urls import path
from . import views

urlpatterns = [
    path('', views.main2, name='main2'),
    path('members/', views.members, name = 'members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),

]