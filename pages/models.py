from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return f"{self.username}"  


class Course(models.Model):
    name = models.CharField(max_length=100)
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class Student(models.Model):
    STATUS_CHOICES = [
        ('present', 'Омадааст'),
        ('absent', 'Наомадааст'),
        ('late', 'Дер кардааст'),
        ('excused', 'Ҷавоб гирифтааст'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='static/images/')
    phone_number = models.CharField(max_length=13) 
    student_course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')  
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User  # or you can use a custom User model
from .models import Student  # If you're using a student model

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)  # Link to Student model
    bio = models.TextField(blank=True, null=True)  # Additional information about the student
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number

    def __str__(self):
        return f"Profile of {self.student.name}"

