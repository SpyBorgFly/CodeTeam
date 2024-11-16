# forms.py
from django import forms
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, SelectMultiple
from .models import Projects, Comment

class ProjectsForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'stack', 'type', 'hashtag', 'is_private', 'is_hidden', 'allowed_users']  # Добавлено поле is_hidden
        widgets = {
            "title": TextInput(attrs={'class': "form-control", 'placeholder': 'Название проекта'}),
            "stack": TextInput(attrs={'class': "form-control", 'placeholder': 'Стэк'}),
            "description": Textarea(attrs={'class': "form-control", 'placeholder': 'Описание'}),
            "type": TextInput(attrs={'class': "form-control", 'placeholder': 'Тип разработки'}),
            "hashtag": TextInput(attrs={'class': "form-control", 'placeholder': 'Хэштеги'}),
            "is_private": CheckboxInput(attrs={'class': "form-check-input"}),
            "is_hidden": CheckboxInput(attrs={'class': "form-check-input"}),  # Новый виджет для is_hidden
            "allowed_users": SelectMultiple(attrs={'class': "form-control"}),
        }

class ProjectFilterForm(forms.Form):
    date_choices = [('recent', 'Недавно добавленные'), ('old', 'Старые проекты')]
    stack_choices = [('python', 'Python'), ('javascript', 'JavaScript'), ('java', 'Java'), ('csharp', 'C#'), ('cpp', 'C++'), ('ruby', 'Ruby'), ('go', 'Go'), ('php', 'PHP')]
    date = forms.ChoiceField(choices=date_choices, required=False)
    stack = forms.ChoiceField(choices=stack_choices, required=False)

class ProjectSettingsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['is_private', 'is_hidden', 'allowed_users']  # Добавлено поле is_hidden
        widgets = {
            'allowed_users': forms.SelectMultiple(attrs={'class': 'chosen-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]