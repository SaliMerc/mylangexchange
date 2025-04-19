from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.forgotten_pass, name='forgotten-pass'),
    path('change-password/', views.change_pass, name='change-pass'),
]