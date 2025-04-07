URL configuration for pet_care_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from pet_care.views import (
    home, register, 
    pet_list, pet_detail, pet_create, pet_edit, pet_delete,
    task_list, task_create, task_edit, task_delete, task_complete,
    expense_list, expense_create, expense_edit, expense_delete,
    reminder_list, reminder_create, reminder_edit, reminder_delete
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('pet_care.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='pet_care/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
    
    # Evcil Hayvan URL'leri
    path('pets/', pet_list, name='pet-list'),
    path('pets/<int:pk>/', pet_detail, name='pet-detail'),
    path('pets/create/', pet_create, name='pet-create'),
    path('pets/<int:pk>/edit/', pet_edit, name='pet-edit'),
    path('pets/<int:pk>/delete/', pet_delete, name='pet-delete'),
    
    # Bakım Görevleri URL'leri
    path('tasks/', task_list, name='task-list'),
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/<int:pk>/edit/', task_edit, name='task-edit'),
    path('tasks/<int:pk>/delete/', task_delete, name='task-delete'),
    path('tasks/<int:pk>/complete/', task_complete, name='task-complete'),
    
    # Harcama URL'leri
    path('expenses/', expense_list, name='expense-list'),
    path('expenses/create/', expense_create, name='expense-create'),
    path('expenses/<int:pk>/edit/', expense_edit, name='expense-edit'),
    path('expenses/<int:pk>/delete/', expense_delete, name='expense-delete'),
    
    # Hatırlatıcı URL'leri
    path('reminders/', reminder_list, name='reminder-list'),
    path('reminders/create/', reminder_create, name='reminder-create'),
    path('reminders/<int:pk>/edit/', reminder_edit, name='reminder-edit'),
    path('reminders/<int:pk>/delete/', reminder_delete, name='reminder-delete'),
]

