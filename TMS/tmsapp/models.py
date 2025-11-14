from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return self.title

class TaskRemark(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="remarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Remark by {self.user.username} on {self.created_at:%Y-%m-%d %H:%M}"
