
from django.contrib.auth.models import User
from projects.models import Projects, Comment, Application
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, UserProfileForm, UserSettingsForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile
from django.http import Http404
from collections import defaultdict


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
        user_profile = get_object_or_404(UserProfile, user=user)
        projects = user.projects.all()
        comments = Comment.objects.filter(author=user).order_by('-created_date')
        outgoing_applications = Application.objects.filter(user=user).order_by('-created_date')
        active_projects = Projects.objects.filter(participants=user)
        is_owner = request.user == user
        starred_projects = user.starred_projects.all()

        
        incoming_applications = Application.objects.filter(project__creator=user, status='pending').order_by('-created_date')

     
        grouped_apps = defaultdict(list)
        for app in incoming_applications:
            grouped_apps[app.project].append(app)

        
        project_requests = []
        for project, apps in grouped_apps.items():
            project_requests.append({
                'project': project,
                'count': len(apps),
                'applications': apps
            })

        return render(request, 'accounts/profile.html', {
            'user': user,
            'projects': projects,
            'comments': comments,
            'outgoing_applications': outgoing_applications,
            'incoming_applications': incoming_applications,
            'active_projects': active_projects,
            'is_owner': is_owner,
            'user_profile': user_profile,
            'project_requests': project_requests,
            'starred_projects': starred_projects
        })

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            raise Http404("Вы не можете редактировать профиль другого пользователя.")
        user_profile = user.userprofile
        form = UserProfileForm(instance=user_profile)
        return render(request, 'accounts/edit_profile.html', {'form': form, 'user_profile': user_profile, 'user': user})

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            raise Http404("Вы не можете редактировать профиль другого пользователя.")
        user_profile = user.userprofile
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
        else:
            print(form.errors)  # Добавляем вывод ошибок
            return render(request, 'accounts/edit_profile.html', {'form': form, 'user_profile': user_profile, 'user': user})

def user_projects(request, username):
    user = get_object_or_404(User, username=username)
    projects = Projects.objects.filter(creator=user)
    return render(request, 'accounts/user_projects.html', {'projects': projects, 'user': user})

@login_required
def delete_project(request, username, project_id):
    user = get_object_or_404(User, username=username)
    project = get_object_or_404(Projects, id=project_id, creator=user)
    if request.method == "POST":
        project.delete()
        return redirect('user_projects', username=user.username)
    return render(request, 'accounts/delete_project_confirm.html', {'project': project, 'user': user})

@login_required
def user_settings(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            # Обновляем информацию о пользователе
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']

            # Если был введен новый пароль, обновляем его
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            if password and new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Чтобы не разлогинился после смены пароля

            user.save()
            return redirect('profile', username=user.username)
    else:
        form = UserSettingsForm(initial={'username': user.username, 'email': user.email})

    return render(request, 'accounts/user_settings.html', {'form': form})

@login_required
def review_applications(request):
    user = request.user
    incoming_applications = Application.objects.filter(project__creator=user, status='pending').order_by('-created_date')
    grouped_apps = defaultdict(list)
    for app in incoming_applications:
        grouped_apps[app.project].append(app)
  
    project_requests = []
    for project, apps in grouped_apps.items():
        project_requests.append({
            'project': project,
            'count': len(apps),
            'applications': apps
        })
    
    return render(request, 'accounts/review_applications.html', {'project_requests': project_requests, 'user': user})