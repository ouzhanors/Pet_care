from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pets', views.PetViewSet, basename='pet')
router.register(r'tasks', views.CareTaskViewSet, basename='task')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
] 