
from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    programming_languages = models.CharField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)

