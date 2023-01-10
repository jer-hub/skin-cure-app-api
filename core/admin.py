from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'first_name','last_name']