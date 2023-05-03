from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Service, Topic, Message

admin.site.register(Service)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
