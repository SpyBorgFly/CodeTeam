from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class UserProfile(models.Model):
    PROGRAMMING_LANGUAGES_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('php', 'PHP'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    programming_languages = MultiSelectField(choices=PROGRAMMING_LANGUAGES_CHOICES, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
