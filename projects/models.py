from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Projects(models.Model):
    title = models.CharField(max_length=200)
    stack = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=100)
    hashtag = models.CharField(max_length=100, blank=True, null=True)
    date_t = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    is_private = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    allowed_users = models.ManyToManyField(User, related_name='allowed_in_projects', blank=True)
    starred_by = models.ManyToManyField(User, related_name='starred_projects', blank=True)
    participants = models.ManyToManyField(User, related_name='participating_projects', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.project}'

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Application by {self.user} for {self.project}'