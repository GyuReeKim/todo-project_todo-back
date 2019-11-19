from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000/api/v1/todos/
    path('todos/', views.todo_create),
]
