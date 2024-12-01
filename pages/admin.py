from django.contrib import admin
from .models import User, Course, Student, Attendance
from .forms import UserForm, CourseForm, StudentForm

admin.site.register([User,Course,Student,Attendance])

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username',)
    ordering = ('username',)


class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ('name', 'time', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('name', 'age', 'phone_number', 'student_course', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'created_at', 'student_course')
    search_fields = ('name', 'phone_number', 'student_course__name')
    ordering = ('-created_at',)
