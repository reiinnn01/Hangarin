import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from manager.models import Task, Note, SubTask, Category, Priority

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_task(50)
        self.create_notes(30)
        self.create_subtask(30)

    def create_task(self, count):
        fake = Faker()
        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        for _ in range(count):
            Task.objects.create(
                title = fake.sentence(nb_words=5),
                status = fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                description = fake.paragraph(nb_sentences=3),
                deadline = timezone.make_aware(fake.date_time_this_month()),
                category = random.choice(categories),
                priority = random.choice(priorities)  
            )
        self.stdout.write(self.style.SUCCESS(
        'Initial data for Task created successfully.'))

    def create_notes(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        for _ in range(count):
            Note.objects.create(
                task = random.choice(tasks),
                content = fake.paragraph(nb_sentences=3)
            )
        self.stdout.write(self.style.SUCCESS(
        'Initial data for note created successfully.'))

    def create_subtask(self, count):
        fake = Faker()
        tasks = list(Task.objects.all())
        for _ in range(count):
            SubTask.objects.create(
                title = fake.sentence(nb_words=5),
                status = fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                parent_task = random.choice(tasks)
            )
        self.stdout.write(self.style.SUCCESS(
        'Initial data for Subtask created successfully.'))