from django.contrib import admin
from .models import Member
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "joined_date",)

admin.site.register(Member, MemberAdmin)