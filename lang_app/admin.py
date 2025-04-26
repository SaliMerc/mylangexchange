from django.contrib import admin
from .models import MyUser, Blog, Course

@admin.register(MyUser)
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name" , "city", "country", "device_info", "is_staff", "is_active")

@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ("blog_author", "blog_title", "blog_content", "blog_image")

@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ("course_name", "course_level", "instructor_name", "difficulty")
