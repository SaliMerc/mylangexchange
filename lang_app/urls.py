from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.forgotten_pass, name='forgotten-pass'),
    path('change-password/', views.change_pass, name='change-pass'),

    path('blogs/', views.blog_list, name='blog-list'),
    path('blogs/blog-content/<slug:slug>', views.blog_single_content, name='blog-single-content'),

    path('login/blogs/', views.blog_logged_in, name='logged-blog'),
    path('login/blogs/blog-content/<slug:slug>/', views.blog_single_post_logged_in, name='blog-single-post-logged-in'),

    path('all-courses/', views.all_courses, name='all-courses'),
    path('courses/enroll/<slug:slug>/', views.enroll_course, name='enroll-course'),

    path('courses/ongoing-courses/', views.ongoing_courses, name='ongoing-courses'),
    path('courses/completed-courses/', views.completed_courses, name='completed-courses'),

    path('courses/learn/<slug:slug>/', views.course_modules, name='course-modules'),
    path('courses/learn/modules/<slug:slug>/', views.module_lessons, name='module-lessons'),
    path('courses/learn/modules/lesson/<slug:slug>/', views.lesson_content, name='lesson-content'),

    path('courses/learn/modules/lesson-completion-status/<slug:slug>/', views.toggle_lesson_completion, name='lesson-complete'),

    path('dashboard/', views.main_dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),

    path('find-partners/', views.find_partners, name='find-partners'),
    path('message-partners/<slug:slug>/', views.message_partners, name='message-partners'),

    path('posts/', views.posts, name='posts'),
    path('posts/add-post/', views.add_post, name='add-post'),
    path('posts/view-posts', views.view_posts, name='view-posts'),

    path('posts/edit-post/<slug:slug>/', views.edit_post, name='edit-post'),
    path('posts/delete-post/<slug:slug>/', views.delete_post, name='delete-post'),

    path('chats/', views.chats, name='chats'),

    path('account/payments/', views.payments, name='payments'),
    path('account/profile-picture/', views.edit_profile_pic, name='edit-profile-picture'),
    path('account/view-profile/', views.view_profile, name='view-profile'),
    path('account/update-profile/', views.update_profile, name='update-profile'),
    path('account/change-password/', views.settings_password_change, name='change-password-in-settings'),
]