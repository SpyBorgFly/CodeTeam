# Generated by Django 5.0.2 on 2024-10-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_projects_date_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='hashtag',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Hashtag'),
        ),
        migrations.AddField(
            model_name='projects',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Тип разработки'),
        ),
    ]