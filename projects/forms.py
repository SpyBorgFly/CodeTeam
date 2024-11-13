from .models import Projects
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django import forms

class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'stack', 'type', 'hashtag']
        widgets = {
            "title": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Название проекта'
            }),
            "stack": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Стэк'
            }),
            "description": Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Описание'
            }),
            "type": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Тип разработки'
            }),
            "hashtag": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Хэштеги'
            }),



        }

class ProjectFilterForm(forms.Form):
    date_choices = [
        ('recent', 'Недавно добавленные'),
        ('old', 'Старые проекты'),
    ]
    
    stack_choices = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('php', 'PHP'),
        
    ]

    date = forms.ChoiceField(choices=date_choices, required=False)
    stack = forms.ChoiceField(choices=stack_choices, required=False)

class ProjectSettingsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['is_private', 'allowed_users']
        widgets = {
            'allowed_users': forms.SelectMultiple(attrs={'class': 'chosen-select'}),
        }