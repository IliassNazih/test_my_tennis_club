from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('login/', views.loginPage, name ="login"),
    path('logout/', views.logoutUser, name ="logout"),
    path('register/', views.registerPage, name ="register"),
    path('infos/', views.infos, name ="infos"),


    path('', views.home, name='home' ),
    path('service/<str:pk>/', views.service, name='service'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),


    path('create-service/', views.createService, name = "create-service"),
    path('update-service/<str:pk>/', views.updateService, name = "update-service"),
    path('delete-service/<str:pk>/', views.deleteService, name = "delete-service"),
    path('map_view/', views.map_view, name='map_view'),
]

urlpatterns += staticfiles_urlpatterns()