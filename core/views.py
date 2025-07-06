from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Course, Enrollment, Student


def home(request):
    courses = Course.objects.all()
    return render(request, 'core/home.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'core/course_detail.html', {'course': course})


@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student, _ = Student.objects.get_or_create(user=request.user)
    Enrollment.objects.get_or_create(student=student, course=course)
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ Create Student profile after user registration
            Student.objects.create(user=user)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    # Ensures Student exists even if somehow it wasn't created at registration
    student, _ = Student.objects.get_or_create(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'dashboard.html', {'enrollments': enrollments})
