from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.register(UserAdmin, Account)
admin.site.register((Account, Blog, Category, Comment, Reply))
