from django import forms
from .models import Course, Lesson, Quiz

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'thumbnail', 'file']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Course Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Course Description'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] focus:outline-none focus:ring transition'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] file:bg-gray-100 dark:file:bg-gray-700 file:text-gray-700 dark:file:text-gray-100 focus:outline-none focus:ring transition'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] file:bg-gray-100 dark:file:bg-gray-700 file:text-gray-700 dark:file:text-gray-100 focus:outline-none focus:ring transition'
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'video_url']

        widgets = {
            'course': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] focus:outline-none focus:ring transition'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Lesson Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Lesson Content'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Optional video URL'
            }),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'course', 'description', 'instructions']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Enter quiz title'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] focus:outline-none focus:ring transition'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Short quiz description'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded bg-[var(--card-color)] text-[var(--text-color)] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring transition',
                'placeholder': 'Optional: quiz instructions'
            }),
        }
