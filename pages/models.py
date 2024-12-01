from django.db import models
import datetime
import numpy as np


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return f"{self.username}"  


class Course(models.Model):
    name = models.CharField(max_length=100) 
    start_time = models.TimeField() 
    end_time = models.TimeField()  


    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    face_image = models.ImageField(upload_to='student_faces/')
    face_encoding = models.BinaryField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=13) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)  # Link to Student model
    bio = models.TextField(blank=True, null=True)  # Additional information about the student
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number

    def __str__(self):
        return f"Profile of {self.student.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField()
    late_minutes = models.IntegerField(null=True, blank=True)
    attendance_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def calculate_lateness(self):
        course_start = datetime.combine(self.attendance_time.date(), self.course.start_time)
        if self.attendance_time > course_start:
            self.late_minutes = (self.attendance_time - course_start).seconds // 60
            self.save()
