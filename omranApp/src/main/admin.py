from django.contrib import admin
from main.models import Products,Command,User
# Register your models here.
admin.site.register(Products)
admin.site.register(Command)
admin.site.register(User)