from django.db import models

# Create your models here.
class Projects(models.Model):

    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    stack = models.TextField('Языки')
    date_t = models.DateTimeField('Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

