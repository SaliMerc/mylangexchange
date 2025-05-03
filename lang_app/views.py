from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from lang_app.models import MyUser, Blog, Post, Course, EnrolledCourses, CourseModule, CourseLesson
from django.contrib.auth.hashers import check_password
import requests
from user_agents import parse as parse_ua

from django.db.models import Min

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

def blog_single_content(request,slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog-single-content.html', {"blog": blog})

def dashboard_base(request):
    return render(request, 'dashboard-base.html')

@login_required
def main_dashboard(request):
    enrolled_courses=EnrolledCourses.objects.filter(student=request.user,is_completed=False).order_by('-enrolment_date')[:3]
    completed_courses = EnrolledCourses.objects.filter(student=request.user,is_completed=True).order_by('-enrolment_date')[:3]
    context={"enrolled_courses":enrolled_courses, "completed_courses":completed_courses}
    return render(request, 'main-dashboard.html', context)

@login_required
def ongoing_courses(request):
    enrolled_courses=EnrolledCourses.objects.filter(student=request.user,is_completed=False).order_by('-enrolment_date')
    context={"enrolled_courses":enrolled_courses}
    return render(request, 'all-ongoing-courses.html', context)

@login_required
def completed_courses(request):
    completed_courses = EnrolledCourses.objects.filter(student=request.user,is_completed=True).order_by('-enrolment_date')
    context={"completed_courses":completed_courses}
    return render(request, 'all-completed-courses.html', context)

@login_required
def logout(request):
    return render(request, 'logout.html')

@login_required
def blog_logged_in(request):
    blogs=Blog.objects.all().order_by('-created_at')
    return render(request, 'blog-logged-in.html', {'blogs':blogs})

@login_required
def blog_single_post_logged_in(request, slug):
    blog=get_object_or_404(Blog, slug=slug)
    return render(request, 'blog-single-content-logged-in.html', {'blog':blog})

@login_required
def all_courses(request):
    courses=Course.objects.all()

    # Getting a list of course IDs that the user is enrolled in
    if request.user.is_authenticated:
        enrolled_course_ids = EnrolledCourses.objects.filter(
            student=request.user,
            is_enrolled=True
        ).values_list('course_name_id', flat=True)
    else:
        enrolled_course_ids = []

    courses_by_language = {}
    for course in courses:
        language = course.course_name
        if language not in courses_by_language:
            courses_by_language[language] = []
        courses_by_language[language].append(course)

    context={'courses':courses,"courses_by_language":courses_by_language,"enrolled_course_ids":enrolled_course_ids}
    return render(request, 'all-courses.html', context)

@login_required
def enroll_course(request,slug):
    course=get_object_or_404(Course, slug=slug)
    if request.method=="POST":
        try:
            student=request.user
            course_name=course
            course_level = course.course_level
            #checking if the student is already enrolled in the course
            already_enrolled = EnrolledCourses.objects.filter(student=student, course_name=course_name, course_level=course_level).exists()

            if already_enrolled:
                messages.error(request, "You are already enrolled in this course.")
            else:
                #to execute if the student is not enrolled yet in the course
                course_enrollment = EnrolledCourses.objects.create(student=student, course_name=course_name, course_level=course_level, is_enrolled=True)
                course_enrollment.save()
                messages.success(request, "You have successfully enrolled!")
                # return redirect("dashboard")
        except Exception as e:
            print(e)
    return render(request, 'enroll-course.html', {"course":course})

@login_required
def course_modules(request,slug):
    my_course = get_object_or_404(
        EnrolledCourses,
        slug=slug,
        student=request.user
    )
    modules = CourseModule.objects.filter(
        course=my_course.course_name
    ).order_by('module_order')
    context={'modules':modules, "my_course":my_course}
    return render(request, 'course-modules-page.html', context)

@login_required
def module_lessons(request,slug):
    module = get_object_or_404(CourseModule,slug=slug)
    lessons = module.module_lessons.all().order_by('lesson_number')
    context={'lessons':lessons, "module":module}
    return render(request, 'module-lessons.html', context)

@login_required
def lesson_content(request,slug):
    current_lesson=get_object_or_404(CourseLesson, slug=slug)

    # Get the next lesson in the same module
    next_lesson = CourseLesson.objects.filter(
        module_name=current_lesson.module_name,  # Same module
        lesson_number__gt=current_lesson.lesson_number  # Higher lesson number
    ).order_by('lesson_number').first()  # Get the first one

    #Get previous lesson
    prev_lesson = CourseLesson.objects.filter(
        module_name=current_lesson.module_name,
        lesson_number__lt=current_lesson.lesson_number
    ).order_by('-lesson_number').first()

    context = {
        "current_lesson": current_lesson,
        "next_lesson": next_lesson,
        "prev_lesson": prev_lesson  # Optional
    }

    return render(request, 'lesson-content-page.html',context)

@login_required
def view_profile(request):
    user=request.user
    return render(request, 'view-profile.html', {"user":user})

@login_required
def update_profile(request):
    user=request.user
    if request.method=="POST":
        try:
            display_name=request.POST.get("display-name")
            if MyUser.objects.filter(display_name=display_name).exists():
                messages.error(request, "This display name is already in use. Please choose another one.")
            else:
                user.display_name=display_name
                user.phone_number=request.POST.get("phone-number")
                user.save()
                messages.success(request, "You have successfully updated your profile.")
        except Exception as e:
            messages.error(request, "An error was encountered while updating your details")
            print(e)
    return render(request, 'update-profile.html',{"user":user})

@login_required
def settings_password_change(request):
    #for changing the password when the user is already logged in
    user=request.user
    if request.method=="POST":
        try:
            old_password=request.POST.get("old-password")
            new_password=request.POST.get("new-password")
            confirm_password=request.POST.get("confirm-password")

            if not check_password(old_password,user.password):
                messages.error(request, "Old password is incorrect.")
            elif new_password == old_password:
                messages.error(request, "New password cannot be same as the old password")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                #for ensuring that the user stays logged in after changing their password
                update_session_auth_hash(request, user)
                messages.success(request, "Your password was successfully updated.")
        except Exception as e:
            print(e)
            messages.error(request, "An error was encountered while updating your password")
    return render(request, 'settings-for-password-update.html',{"user":user})

@login_required
def edit_profile_pic(request):
    user=request.user
    if request.method=="POST":
        try:
            if 'profile-picture' in request.FILES:
                user.profile_picture = request.FILES['profile-picture']
                user.save()
                messages.success(request, "Your profile picture has been updated successfully.")
            else:
                messages.error(request, "No new profile picture uploaded.")

        except Exception as e:
            print(e)
            messages.error(request, "An error was encountered while updating the profile picture")
    return render(request, 'edit-profile-picture.html')

@login_required
def payments(request):
    return render(request, 'payments.html')

@login_required
def find_partners(request):
    languages = (
        Course.objects
        .values('course_name')
        .annotate(min_id=Min('id'))
        .order_by('course_name')
    )
    users = MyUser.objects.filter(
        id__in=EnrolledCourses.objects.values('student').distinct().exclude(student=request.user)
    ).prefetch_related(
        Prefetch(
            'students',
            queryset=EnrolledCourses.objects.select_related('course_name')
            .order_by('-enrolment_date'),
            to_attr='user_courses'
        )
    )

    query=request.GET.get('q')
    if query:
        users = MyUser.objects.filter(
            id__in=EnrolledCourses.objects.values('student').distinct().exclude(student=request.user).filter(course_name__course_name__icontains=query)
        ).prefetch_related(
            Prefetch(
                'students',
                queryset=EnrolledCourses.objects.select_related('course_name')
                .order_by('-enrolment_date'),
                to_attr='user_courses'
            )
        )
    context={"users":users,"languages":languages, "query":query}
    return render(request, 'find-partners.html', context)

@login_required
def message_partners(request, slug):
    partner=get_object_or_404(MyUser, slug=slug)
    return render(request, 'message-partners.html',{"partner":partner})

@login_required
def posts(request):
    return render(request, 'posts.html')

@login_required
def add_post(request):
    return render(request,'add-post.html')

@login_required
def chats(request):
    return render(request, 'chats.html')