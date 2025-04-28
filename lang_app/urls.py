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
    path('courses/enroll/<int:id>/', views.enroll_course, name='enroll-course'),

    path('courses/ongoing-courses/', views.ongoing_courses, name='ongoing-courses'),
    path('courses/completed-courses/', views.completed_courses, name='completed-courses'),

    path('courses/learn/<int:id>/', views.course_modules, name='course-modules'),
    path('courses/learn/modules/<int:id>/', views.module_lessons, name='module-lessons'),
    path('courses/learn/modules/lesson/<int:id>/', views.lesson_content, name='lesson-content'),


    path('dashboard/', views.main_dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    path('find-partners/', views.find_partners, name='find-partners'),
    path('posts/', views.posts, name='posts'),
    path('chats/', views.chats, name='chats'),

    path('account/payments/', views.payments, name='payments'),
    path('account/profile-picture/', views.edit_profile_pic, name='edit-profile-picture'),
    path('account/view-profile/', views.view_profile, name='view-profile'),
    path('account/update-profile/', views.update_profile, name='update-profile'),
    path('account/change-password/', views.settings_password_change, name='change-password-in-settings'),
]