from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.forgotten_pass, name='forgotten-pass'),
    path('change-password/', views.change_pass, name='change-pass'),

    path('blogs/', views.blog_list, name='blog-list'),
    path('blogs/blog-content/', views.blog_single_content, name='blog-single-content'),

    path('dashboard/', views.main_dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]