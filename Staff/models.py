from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Task(models.Model):
    # name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Pending')
    # assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - Assigned to {self.member.username}"
    # name = models.CharField(max_length=255)
    # member = models.ForeignKey(User, on_delete=models.CASCADE)

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)