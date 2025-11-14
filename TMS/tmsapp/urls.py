from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/new/', views.create_task, name='task_new'),
    path('task/<int:task_id>/edit/', views.edit_task, name='task_edit'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
