from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, SubTask, Note, Priority, Category, STATUS_CHOICES
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.list import ListView

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "Task.html"

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(category__icontains=query) |
                Q(status__icontains=query)
            )
        return qs 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        selected_id = self.request.GET.get('selected')
        selected_task = None
        if selected_id:
            selected_task = Task.objects.filter(id=selected_id).first()
            
        context['selected_task'] = selected_task
        context['priorities'] = Priority.objects.all()
        context['categories'] = Category.objects.all()
        context["status_choices"] = STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        task_id = request.POST.get('task_id')

        if action == 'create':
            title = request.POST.get('title')
            if title:
                default_priority = Priority.objects.first()
                def_category = Category.objects.first()
                Task.objects.create(
                    title=title,
                    status='Pending',
                    priority=default_priority,
                    category=def_category
                )
            return redirect('task-list')
        
        elif action == 'update':
            task = get_object_or_404(Task, id=task_id)
            task.title = request.POST.get('title')
            task.status = request.POST.get('status')
            priority_id = request.POST.get('priority')
            task.priority_id = priority_id if priority_id else None
            
            deadline = request.POST.get('deadline')
            task.deadline = deadline if deadline else None
            task.save()
            return redirect(f'/Tasks/?selected={task.id}')

        elif action == 'delete':
            Task.objects.filter(id=task_id).delete()
            return redirect('task-list')

        return redirect('task-list')
    
class SubTaskView(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = "SubTask.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_id = self.request.GET.get('selected')
        selected_subtask = None
        if selected_id:
            selected_subtask=SubTask.objects.filter(id=selected_id).first()

        context['selected_subtask'] = selected_subtask
        context["status_choices"] = STATUS_CHOICES
        context['tasks'] = Task.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        subtask_id = request.POST.get('subtask_id')

        if action == 'create':
            title = request.POST.get('title')
            if title:
                SubTask.objects.create(
                   title = title,
                   status = 'Pending'
                )
            return redirect('subtask-list')
        
        elif action == "update":
            subtask = get_object_or_404(SubTask, id=subtask_id)
            subtask.parent_task_id = request.POST.get('parent_task_id')
            subtask.title = request.POST.get('title')
            subtask.status = request.POST.get('status')
            subtask.save()
            return redirect(f"/Subtasks/?selected={subtask.id}")

        elif action == "delete":
            SubTask.objects.filter(id=subtask_id).delete()
            return redirect('subtask-list')

        return redirect('subtask-list')


class NoteView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = "Note.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_id = self.request.GET.get("selected")
        selected_note = None
        if selected_id:
            selected_note = Note.objects.filter(id=selected_id).first()

        context["selected_note"] = selected_note
        context["tasks"] = Task.objects.all()
        return context
        

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        note_id = request.POST.get("note_id")

        if action == 'create':
            content = request.POST.get('content')
            if content:
                Note.objects.create(
                   content = content
                )
            return redirect('note-list')
        
        elif action == "update":
            note = get_object_or_404(Note, id=note_id)
            note.task_id = request.POST.get('task_id')
            note.content = request.POST.get('content')
            note.save()
            return redirect(f"/Notes/?selected={note.id}")
        elif action == "delete":
            Note.objects.filter(id=note_id).delete()
            return redirect('note-list')

        return redirect('note-list')


        


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = "Category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_id = self.request.GET.get('selected')
        selected_category = None
        if selected_id:
            selected_category = Category.objects.filter(id=selected_id).first()

        context['selected_category'] = selected_category
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        category_id = request.POST.get('category_id')

        if action == 'create':
            name = request.POST.get('name')
            if name:
                Category.objects.create(
                    category_name = name
                )
            return redirect('category-list')
        
        elif action == "update":
            category = get_object_or_404(Category, id=category_id)
            category.category_name = request.POST.get('category_name')
            category.save()
            return redirect(f'/Categories/?selected={category.id}')
        
        elif action == "delete":
            Category.objects.filter(id=category_id).delete()
            return redirect('category-list')
        
        return redirect('category-list')


class PriorityView(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = "Priority.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_id = self.request.GET.get('selected')
        selected_priority = None
        if selected_id:
            selected_priority = Priority.objects.filter(id=selected_id).first()

        context['selected_priority'] = selected_priority
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        priority_id = request.POST.get('priority_id')

        if action == 'create':
            name = request.POST.get('name')
            if name:
                Priority.objects.create(
                    priority_name = name
                )
            return redirect('priority-list')
        
        if action == "update":
            priority = get_object_or_404(Priority, id=priority_id)
            priority.priority_name = request.POST.get('priority_name')
            priority.save()
            return redirect(f"/Priorities/?selected={priority_id}")
        elif action == "delete":
            Priority.objects.filter(id=priority_id).delete()
            return redirect('priority-list')
        return redirect('priority-list')
