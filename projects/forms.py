from .models import Projects
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'stack']
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
            })


        }
