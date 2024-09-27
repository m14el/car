from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Car, Comment

admin.site.register(Car)
admin.site.register(Comment)