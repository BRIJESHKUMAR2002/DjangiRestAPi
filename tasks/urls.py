from django.urls import path
from .views import RegisterView, LoginView,TaskCreateView,TaskListView, TaskDetailView, TaskMemberAddRemoveView, TaskMemberListView, UpdateTaskStatusView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:task_id>/members/', TaskMemberListView.as_view(), name='task-member-list'),
    path('tasks/<int:task_id>/members/add/', TaskMemberAddRemoveView.as_view(), name='task-member-add'),
    path('tasks/<int:task_id>/members/remove/', TaskMemberAddRemoveView.as_view(), name='task-member-remove'),
    path('tasks/<int:task_id>/status/', UpdateTaskStatusView.as_view(), name='task-status-update'),
]
