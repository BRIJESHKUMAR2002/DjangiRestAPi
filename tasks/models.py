from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = (
        ('Todo', 'Todo'),
        ('Inprogress', 'Inprogress'),
        ('Done', 'Done'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Todo')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class TaskMember(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.task.title}'
