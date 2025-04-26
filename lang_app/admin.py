from django.contrib import admin
from .models import MyUser, Blog

@admin.register(MyUser)
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name" , "city", "country", "device_info", "is_staff", "is_active")

@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ("blog_author", "blog_title", "blog_content", "blog_image")
