from django.contrib import admin

from .models import Priority, Category, Task, Note, SubTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "deadline", "priority", "category"]
    search_fields = ["title", "description"]
    list_filter =["status", "priority", "category"]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "parent_task_name"]
    search_fields = ["title"]
    list_filter = ["status"]

    @admin.display(description='parent task')
    def parent_task_name(self, obj):
        if obj.parent_task:
            return obj.parent_task.title
        return None
        

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name"]
    search_fields =  ["category_name"]
   

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ["priority_name"]
    search_fields = ["priority_name"]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["get_task", "content", "created_at" ]
    search_fields = ["content"]
    list_filter = ["created_at"]

    @admin.display(description='Assigned To Task')
    def get_task(self, obj):
        if obj.task:
            return obj.task.title
        return None