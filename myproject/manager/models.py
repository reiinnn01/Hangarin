from django.db import models

class basemodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        abstract = True

class Priority(basemodel):
    Priority_Name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Priorities"  

    def __str__(self):
        return self.Priority_Name

class Category(basemodel):
    category_name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
    
class Task(basemodel):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    deadline = models.DateField(auto_now_add=True)
    status = models.CharField(
    max_length=50,
    choices=[
        ("Pending", "Pending"),
        ("In Progress ", "In Progress"),
        ("Completed", "Completed"),
    ],
    default="pending"
    )
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
            return self.title
    

class Note(basemodel):
    task = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.task

class SubTask(basemodel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=50,
    choices=[
            ("Pending", "Pending"),
            ("In Progress ", "In Progress"),
            ("Completed", "Completed"),
    ],
    default="pending"
    )

    def __str__(self):
        return self.title

