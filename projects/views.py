from django.shortcuts import render, redirect
from .models import Projects
from .forms import ProjectsForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
def all_projects(request):
    projects = Projects.objects.all()
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