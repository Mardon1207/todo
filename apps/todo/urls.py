from django.urls import path
from .views import TodosView,TodosItemView,TasksView,TasksItemView


urlpatterns = [
    path('todos/', TodosView.as_view()),
    path('todos/<int:todo_id>/', TodosItemView.as_view()),
    path('todos/<int:todo_id>/tasks', TasksView.as_view()),
    path('todos/<int:todo_id>/tasks/<int:task_id>', TasksItemView.as_view()),
]
