from django.http import JsonResponse
from .models import Projects, Comment, Application
from .forms import ProjectsForm, ProjectFilterForm, ProjectSettingsForm, CommentForm, ReplyForm, ApplicationForm
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.db.models import Q

def clean_html(description):
    allowed_tags = [
        'p', 'a', 'strong', 'em', 'table', 'tr', 'td', 'th', 'img', 'span', 'colgroup', 'col', 'tbody'
    ]
    allowed_attributes = {
        '*': ['style'],  # Разрешаем атрибут style для всех тегов
        'a': ['href', 'title'],  # Разрешаем атрибуты для <a>
        'img': ['src', 'alt'],  # Разрешаем атрибуты для <img>
        'table': ['width', 'border', 'cellspacing', 'cellpadding'],  # Разрешаем атрибуты для <table>
        'col': ['style'],  # Разрешаем атрибут style для <col>
    }
    return bleach.clean(description, tags=allowed_tags, attributes=allowed_attributes)

def all_projects(request):
    projects = Projects.objects.all()

    if request.user.is_authenticated:
        projects = projects.filter(
            Q(is_hidden=False) | 
            Q(creator=request.user) | 
            Q(allowed_users=request.user)
        )
    else:
        projects = projects.filter(is_hidden=False)

    projects_with_access = []

    for project in projects:
        has_access = (
            not project.is_private or 
            (request.user.is_authenticated and (
                project.creator == request.user or 
                request.user in project.allowed_users.all()
            ))
        )
        projects_with_access.append({
            'project': project,
            'has_access': has_access
        })

    # Фильтрация по GET-параметрам
    hashtag = request.GET.get('hashtag')
    stack = request.GET.get('stack')
    custom_stack = request.GET.get('custom_stack')
    type_dev = request.GET.get('type')
    date = request.GET.get('date')

    if hashtag:
        projects = projects.filter(hashtag__icontains=hashtag)
    if stack:
        projects = projects.filter(stack__iexact=stack)
    if custom_stack:
        projects = projects.filter(stack__iexact=custom_stack)
    if type_dev:
        projects = projects.filter(type__icontains=type_dev)
    if date:
        if date == 'recent':
            projects = projects.order_by('-date_t')
        elif date == 'old':
            projects = projects.order_by('date_t')

    context = {
        'projects_with_access': projects_with_access
    }
    return render(request, 'projects/all_projects.html', context)

class ProjectsDetailView(DetailView):
    model = Projects
    template_name = 'projects/details_view.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        user = self.request.user
        
        context['comments'] = Comment.objects.filter(project=project, parent__isnull=True)
        context['comment_form'] = CommentForm()
        context['reply_form'] = ReplyForm()
        context['application_form'] = ApplicationForm()  # Добавляем форму заявки
        context['has_access'] = self.request.user == project.creator or not(project.is_private)
        
        # Добавляем проверки для кнопки подачи заявки
        context['is_creator'] = user == project.creator
        context['is_participant'] = project.allowed_users.filter(pk=user.pk).exists()
        context['has_applied'] = Application.objects.filter(project=project, user=user).exists()
        
        return context

@login_required
def add_comment(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            return redirect('project-details', pk=project.pk)
    return redirect('project-details', pk=project.pk)

@login_required
def add_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.project = parent_comment.project
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            return redirect('project-details', pk=parent_comment.project.pk)
    return redirect('project-details', pk=parent_comment.project.pk)

@login_required
def add_projects(request):
    error = ''
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.date_t = timezone.now()

            # Очищаем описание перед сохранением
            project.description = clean_html(project.description)

            project.save()
            return redirect('all_projects')  
        else:
            error = 'ошибка'

    form = ProjectsForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'projects/add_projects.html', data)

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)  # Сохраняем изображение в media
        uploaded_file_url = fs.url(filename)  # URL для доступа к изображению
        return JsonResponse({'url': uploaded_file_url})
    return JsonResponse({'error': 'No image uploaded'}, status=400)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Projects
    form_class = ProjectsForm
    template_name = 'projects/edit_project.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse_lazy('project-details', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.creator != self.request.user:
            return redirect('project-details', pk=obj.pk)
        return obj

@method_decorator(login_required, name='dispatch')
class ProjectSettingsView(View):
    def get(self, request, pk):
        project = get_object_or_404(Projects, pk=pk)
        if request.user != project.creator:
            return redirect('project_details', pk=project.pk)
        form = ProjectSettingsForm(instance=project)
        return render(request, 'projects/project_settings.html', {'form': form, 'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Projects, pk=pk)
        if request.user != project.creator:
            return redirect('project_details', pk=project.pk)
        form = ProjectSettingsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-details', pk=project.pk)
        return render(request, 'projects/project_settings.html', {'form': form, 'project': project})

@login_required
def apply_to_project(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    user = request.user
    
    # Проверяем, является ли пользователь создателем проекта
    if user == project.creator:
        return JsonResponse({'success': False, 'message': 'Вы не можете подать заявку на свой собственный проект.'})
    
    # Проверяем, уже подал ли пользователь заявку на этот проект
    if Application.objects.filter(project=project, user=user).exists():
        return JsonResponse({'success': False, 'message': 'Вы уже подали заявку на этот проект.'})
    
    # Проверяем, является ли пользователь уже участником проекта
    if project.allowed_users.filter(pk=user.pk).exists():
        return JsonResponse({'success': False, 'message': 'Вы уже являетесь участником этого проекта.'})
    
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.user = user
            application.save()
            return JsonResponse({'success': True, 'message': 'Ваша заявка успешно подана!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ApplicationForm()
    return render(request, 'projects/apply_to_project.html', {'form': form, 'project': project})


@login_required
def accept_application(request, pk, app_id):
    application = get_object_or_404(Application, pk=app_id, project__pk=pk)
    if request.user != application.project.creator:
        return JsonResponse({'success': False, 'message': 'Вы не можете принять эту заявку.'})
    application.status = 'accepted'
    application.save()
    project = application.project
    project.allowed_users.add(application.user)
    return JsonResponse({'success': True, 'message': 'Заявка успешно принята.'})

@login_required
def reject_application(request, pk, app_id):
    application = get_object_or_404(Application, pk=app_id, project__pk=pk)
    if request.user != application.project.creator:
        return JsonResponse({'success': False, 'message': 'Вы не можете отклонить эту заявку.'})
    application.status = 'rejected'
    application.save()
    return JsonResponse({'success': True, 'message': 'Заявка успешно отклонена.'})