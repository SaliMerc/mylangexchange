from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from lang_app.models import MyUser, Blog, Post
from django.contrib.auth.hashers import check_password
import requests
from user_agents import parse as parse_ua

# api starts here
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {
            "country": data.get("country", "Unknown"),
            "city": data.get("city", "Unknown"),
        }
    except Exception:
        return {"country": "Unknown", "city": "Unknown"}

def get_device_info(request):
    user_agent_str = request.headers.get("User-Agent", "")
    user_agent = parse_ua(user_agent_str)
    return f"{user_agent.browser.family} on {user_agent.os.family} ({user_agent.device.family})"
 # api ends here



def base(request):
    return render(request, 'base-main.html')

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        try:
            full_name=request.POST.get('full-name').strip()
            name=full_name.split()
            if name:
                first_name = name[0]
            else:
                messages.error(request, 'Please enter your full name.')
            if len(name) > 1:
                last_name = " ".join(name[1:])
            else:
                messages.error(request, 'Please enter your full name.')

            email = request.POST.get("email")
            password = request.POST.get("password")
            conf_pass = request.POST.get("c-password")
            display_name = request.POST.get("display-name")
            if MyUser.objects.filter(display_name=display_name).exists():
                messages.error(request, 'A user with this display name already exists, kindly choose another name')
            if MyUser.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists')
                return render(request, "login.html")
            if password != conf_pass:
                messages.error(request, 'Passwords do not match')
                return render(request, "signup.html")
            my_user = MyUser.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
            )
            my_user.set_password(password)

            ip = get_client_ip(request)
            geo = get_geo_info(ip)
            device = get_device_info(request)

            my_user.country = geo["country"]
            my_user.city = geo["city"]
            my_user.device_info = device
            my_user.save()
            return redirect('login')
        except Exception as e:
            print(e)
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email").strip()
            password = request.POST.get("password")

            if not email or not password:
                messages.error(request, "Both email and password are required!")
                return redirect('login')

            user_exists = MyUser.objects.filter(email=email).exists()

            if not user_exists:
                messages.error(request, "Email not found! Please check your email or register.")
                return redirect('signup')

            # Authenticate
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Incorrect password!")
                return redirect('login')
        except Exception as e:
            print(e)
    return render(request, 'login.html')

def forgotten_pass(request):
    return render(request, 'forgotten-password.html')

def change_pass(request):
    return render(request, 'change-password.html')

def blog_list(request):
    blogs=Blog.objects.all().order_by('-created_at')
    return render(request, 'blog.html',{'blogs':blogs})

def blog_single_content(request,id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog-single-content.html', {"blog": blog})

def dashboard_base(request):
    return render(request, 'dashboard-base.html')

@login_required
def main_dashboard(request):
    user = request.user
    context={"user":user}
    return render(request, 'main-dashboard.html', context)

@login_required
def logout(request):
    return render(request, 'logout.html')

@login_required
def blog_logged_in(request):
    blogs=Blog.objects.all().order_by('-created_at')
    return render(request, 'blog-logged-in.html', {'blogs':blogs})

@login_required
def blog_single_post_logged_in(request, id):
    blog=get_object_or_404(Blog, id=id)
    return render(request, 'blog-single-content-logged-in.html', {'blog':blog})