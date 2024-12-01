from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('create-student/', create_student, name='create_student'), 
    path('students/', student_list, name='student_list'),
    path('students/edit/<int:id>/',update_student, name='update_student'),
    path('students/delete/<int:id>/',delete_student, name='delete_student'),
    path('courses/',course_list, name='course_list'),
    path('courses/create/',create_course, name='create_course'),
    path('courses/update/<int:id>/',update_course, name='update_course'),
    path('courses/delete/<int:id>/',delete_course, name='delete_course'),
    path('profile/<int:student_id>/',profile_view, name='profile_view'),

]