from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import StudentForm  # Import the StudentForm
from .models import Student  # Import the Student model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = UserCreationForm()  

    return render(request, 'register.html', {'form': form})  


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Номи корбар ё гузарвожа нодуруст аст")
            return render(request, 'login.html')  
    
    return render(request, 'login.html') 


def home(request):
    if not request.user.is_authenticated: 
        return redirect('login')  
    
    student_count = Student.objects.count()  # Öğrenci sayısını al
    attended_count = Student.objects.filter(attendance=True).count()  # Katılan öğrenci sayısını al
    not_attended_count = Student.objects.filter(attendance=False).count()  # Katılmayan öğrenci sayısını al
    return render(request, 'home.html', {'student_count': student_count, 'attended_count': attended_count, 'not_attended_count': not_attended_count})  # Öğrenci sayısını, katılan sayısını ve katılmayan sayısını template'e geçir


def logout_view(request):
    logout(request)  
    return redirect('login')  


def create_student(request):
    if not request.user.is_authenticated:  
        return redirect('login')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully!")
            return redirect('home')  
        else:
            messages.error(request, "Error creating student. Please check the form and try again.")
    else:
        form = StudentForm()

    return render(request, 'create_student.html', {'form': form})



# View to list all students
def student_list(request):
    students = Student.objects.select_related('course').all().count()

    return render(request, 'student_list.html', {'students': students})


# View to update student
def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


# View to create a new course
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

# View to update a course
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

# View to delete a course
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('course_list')

from django.shortcuts import render, get_object_or_404
from .models import Student, Profile
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Profile

from django.shortcuts import render, get_object_or_404
from .models import Student

def profile_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'profile_view.html', {'student': student})