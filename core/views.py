from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    UserChangeForm, PasswordChangeForm
)

from .models import Course, Enrollment, Student, Lesson, Quiz
from .forms import CourseForm, LessonForm, QuizForm

# ---------------------- Home ----------------------

def home(request):
    if request.user.is_authenticated:
        return redirect('chat:inbox')
    courses = Course.objects.all()
    return render(request, 'core/home.html', {'courses': courses})

# ---------------------- Course Views ----------------------

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'core/course_detail.html', {'course': course})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {
        'form': form,
        'form_title': 'Create Course',
        'button_text': 'Create'
    })

@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {
        'form': form,
        'form_title': 'Edit Course',
        'button_text': 'Update'
    })

# ---------------------- Lesson Views ----------------------

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'core/lesson_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'core/lesson_detail.html', {'lesson': lesson})

@login_required
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson created successfully.')
            return redirect('dashboard')
    else:
        form = LessonForm()
    return render(request, 'core/lesson_form.html', {
        'form': form,
        'form_title': 'Create Lesson',
        'button_text': 'Create'
    })

# ---------------------- Quiz Views ----------------------

@login_required
def quiz_page(request):
    return render(request, 'core/quiz.html')

@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz created successfully.')
            return redirect('dashboard')
    else:
        form = QuizForm()
    return render(request, 'core/quiz_form.html', {
        'form': form,
        'form_title': 'Create Quiz',
        'button_text': 'Create Quiz'
    })

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'core/quiz_list.html', {'quizzes': quizzes})

# Optional: Add a quiz detail view if needed
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'core/quiz_detail.html', {'quiz': quiz})

# ---------------------- Enrollment ----------------------

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student, _ = Student.objects.get_or_create(user=request.user)
    Enrollment.objects.get_or_create(student=student, course=course)
    return redirect('dashboard')

# ---------------------- Dashboard ----------------------

@login_required
def dashboard(request):
    student, _ = Student.objects.get_or_create(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    lessons = Lesson.objects.all()
    quizzes = Quiz.objects.all()
    return render(request, 'dashboard.html', {
        'enrollments': enrollments,
        'lesson_list': lessons,
        'quiz_list': quizzes
    })

# ---------------------- Authentication ----------------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            login(request, user)
            return redirect('chat:inbox')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:inbox')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# ---------------------- Profile & Password ----------------------

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# ---------------------- AJAX: Live Profile Update ----------------------

@login_required
def update_profile_ajax(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
