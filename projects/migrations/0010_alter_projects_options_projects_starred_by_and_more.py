# Generated by Django 5.0.2 on 2024-12-10 20:59

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_application'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={},
        ),
        migrations.AddField(
            model_name='projects',
            name='starred_by',
            field=models.ManyToManyField(blank=True, related_name='starred_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Ожидание'), ('accepted', 'Принято'), ('rejected', 'Отклонено')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='projects',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_in_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_t',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='projects',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='projects',
            name='hashtag',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='stack',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='projects',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='projects',
            name='type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]