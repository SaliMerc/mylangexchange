from django.shortcuts import render

def base(request):
    return render(request, 'base-main.html')

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def forgotten_pass(request):
    return render(request, 'forgotten-password.html')

def change_pass(request):
    return render(request, 'change-password.html')