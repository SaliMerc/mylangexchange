from django.contrib import admin
from .models import MyUser

@admin.register(MyUser)
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name" , "city", "country", "device_info", "is_staff", "is_active")
