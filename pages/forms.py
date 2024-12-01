from django import forms
from .models import *


class UserForm(forms.ModelForm):  
    class Meta:
        model = User
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo', 'phone_number']
