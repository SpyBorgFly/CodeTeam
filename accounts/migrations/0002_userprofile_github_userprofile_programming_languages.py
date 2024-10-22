# Generated by Django 5.1.2 on 2024-10-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='programming_languages',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
