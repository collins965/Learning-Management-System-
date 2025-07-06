from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    # Authentication routes
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Course enrollment
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_course'),

    # Student dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
