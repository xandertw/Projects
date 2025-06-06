from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path('create_task/', views.create_task),
    path('get_tasks/', views.get_tasks),
    path('get_overdue_tasks/', views.get_overdue_tasks),
    path('delete_task/<int:task_id>/', views.delete_task),
    path('login/', login, name='login'),  
]