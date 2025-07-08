from django.urls import path
from . import views

urlpatterns = [
    #  Home & Courses 
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:course_id>/edit/', views.course_edit, name='course_edit'),

    #  Lessons 
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),

    #  Quizzes           
    path('quiz/create/', views.quiz_create, name='quiz_create'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),

    #  Enrollment & Dashboard 
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_course'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # User Profile 
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/update/', views.update_profile_ajax, name='update_profile_ajax'),

    #  Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
