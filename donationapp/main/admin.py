from django.contrib import admin

# Register your models here.
from .models import Main
from django.contrib.auth.models import Permission

admin.site.register(Main)
admin.site.register(Permission)
