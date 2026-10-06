from django.contrib import admin
from django.urls import path, include
from .views import TaskView, SubTaskView, NoteView, CategoryView, PriorityView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include("allauth.urls")),
    path('', TaskView.as_view(), name='home'),
    path('Tasks/', TaskView.as_view(), name='task-list'),
    path('Subtasks/', SubTaskView.as_view(), name='subtask-list'),
    path('Notes/', NoteView.as_view(), name='note-list')    ,
    path('Categories/', CategoryView.as_view(), name='category-list'),
    path('Priorities/', PriorityView.as_view(), name='priority-list'),
]   