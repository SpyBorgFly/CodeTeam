from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'programming_languages', 'github', 'avatar']  
        widgets = {
            'programming_languages': forms.SelectMultiple(attrs={'class': 'select2'}),
        }
        # Переопределим поля, чтобы сделать их необязательными:
        widgets = {
            'programming_languages': forms.SelectMultiple(attrs={'class': 'select2'}),
        }
    
    # Зададим все поля как необязательные:
    bio = forms.CharField(required=False)
    location = forms.CharField(required=False)
    programming_languages = forms.MultipleChoiceField(choices=UserProfile.PROGRAMMING_LANGUAGES_CHOICES, required=False)
    github = forms.URLField(required=False)
    avatar = forms.ImageField(required=False)

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        # Проверяем, что новые пароли совпадают
        if new_password and new_password != confirm_new_password:
            raise forms.ValidationError("Новые пароли не совпадают.")
        
        # Если пароль не указан, но новые пароли указаны, то ошибка
        if (new_password or confirm_new_password) and not password:
            raise forms.ValidationError("Введите текущий пароль для изменения пароля.")
        
        return cleaned_data
    
