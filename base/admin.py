from django.contrib import admin

from .models import Service, Topic, Message

admin.site.register(Service)
admin.site.register(Topic)
admin.site.register(Message)


# Register your models here.
