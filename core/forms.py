from django import forms
from .models import Course, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'thumbnail', 'file']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Course Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Course Description'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
            }),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'video_url']

        widgets = {
            'course': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Lesson Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Lesson Content'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Optional video URL'
            }),
        }
