from django.contrib.auth.models import User

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)

        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', username=user.username)
        return render(request, 'accounts/login.html', {'error': 'Неверное имя пользователя или пароль'})




class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        projects = user.projects.all()
        return render(request, 'accounts/profile.html', {'user': user, 'projects': projects})

