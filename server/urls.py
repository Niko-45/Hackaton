"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
 

from django.contrib import admin
from django.urls import path
from pages import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('', views.home, name='home'),  
    path('create_student/', views.create_student, name='create_student'),  
    path('students/', views.student_list, name='student_list'),
    path('students/edit/<int:id>/', views.update_student, name='update_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/update/<int:id>/', views.update_course, name='update_course'),
    path('courses/delete/<int:id>/', views.delete_course, name='delete_course'),
    path('profile/<int:student_id>/', views.profile_view, name='profile_view'),
    ]
