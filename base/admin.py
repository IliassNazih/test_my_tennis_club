from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Service, Topic, Message,Adresse

admin.site.register(Service)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Adresse)

class AddressInline(admin.StackedInline):
    model = Adresse
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [AddressInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Register your models here.
