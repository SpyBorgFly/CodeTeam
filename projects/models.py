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
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


