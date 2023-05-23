from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Service, Topic, Message

class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Service, ServiceAdmin)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
