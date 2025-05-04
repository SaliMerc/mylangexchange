from django.contrib import admin
from .models import MyUser, Blog, Course, EnrolledCourses, CourseModule, CourseLesson,Post

@admin.register(MyUser)
class MyUserModelAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name" , "city", "country", "device_info", "is_staff", "is_active")

@admin.register(Blog)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ("blog_author", "blog_title", "blog_content", "blog_image")

@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ("course_name", "course_level", "instructor_name", "difficulty")

@admin.register(EnrolledCourses)
class EnrolledCourseModelAdmin(admin.ModelAdmin):
    list_display = ("student", "course_name","course_level", "enrolment_date", "is_enrolled", "completion_date")

@admin.register(CourseModule)
class CourseModuleModelAdmin(admin.ModelAdmin):
    list_display = ("course","module_title", "module_description","module_order")

@admin.register(CourseLesson)
class CourseLessonModelAdmin(admin.ModelAdmin):
    list_display = ("module_name", "lesson_description","lesson_content","lesson_type","lesson_file","lesson_number")

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ("post_author","post_content","post_images")
