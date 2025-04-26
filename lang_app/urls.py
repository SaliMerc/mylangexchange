from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.forgotten_pass, name='forgotten-pass'),
    path('change-password/', views.change_pass, name='change-pass'),

    path('blogs/', views.blog_list, name='blog-list'),
    path('blogs/blog-content/<int:id>', views.blog_single_content, name='blog-single-content'),

    path('login/blogs/', views.blog_logged_in, name='logged-blog'),
    path('login/blogs/blog-content/<int:id>/', views.blog_single_post_logged_in, name='blog-single-post-logged-in'),

    path('all-courses/', views.all_courses, name='all-courses'),
    path('courses/enroll', views.enroll_course, name='enroll-course'),

    path('dashboard/', views.main_dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]