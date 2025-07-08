from django.contrib import admin
from .models import Course, Lesson, Enrollment, Student, Quiz

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Student)
admin.site.register(Quiz)
