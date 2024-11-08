from django.shortcuts import render, redirect
from .models import Projects
from .forms import ProjectsForm, ProjectFilterForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import bleach

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
    
    # Фильтрация по хештегам
    hashtag = request.GET.get('hashtag')
    if hashtag:
        projects = projects.filter(hashtag__icontains=hashtag)

    # Фильтрация по языку программирования
    stack = request.GET.get('stack')
    custom_stack = request.GET.get('custom_stack')
    if stack and stack != 'Other':
        projects = projects.filter(stack__icontains=stack)
    elif custom_stack:
        projects = projects.filter(stack__icontains=custom_stack)

    # Фильтрация по типу разработки
    project_type = request.GET.get('type')
    if project_type:
        projects = projects.filter(type__icontains=project_type)

    # Фильтрация по дате
    date_filter = request.GET.get('date')
    if date_filter == 'recent':
        projects = projects.order_by('-date_t')
    elif date_filter == 'old':
        projects = projects.order_by('date_t')

    return render(request, 'projects/all_projects.html', {'projects': projects})

class ProjectsDetailView(DetailView):
    model = Projects
    template_name = 'projects/details_view.html'
    context_object_name = 'project'


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
