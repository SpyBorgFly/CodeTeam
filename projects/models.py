from django.db import models
from  django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Projects(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    stack = models.TextField('Языки')
    date_t = models.DateTimeField(default=timezone.now, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    type = models.CharField('Тип разработки', max_length=50, blank=True, null=True)
    hashtag = models.CharField('Hashtag', max_length=50, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    allowed_users = models.ManyToManyField(User, related_name='allowed_projects', blank=True)
    is_hidden = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Comment(models.Model):
    project = models.ForeignKey(Projects, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.project}'