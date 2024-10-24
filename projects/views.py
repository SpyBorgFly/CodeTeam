from django.shortcuts import render, redirect
from .models import Projects
from .forms import ProjectsForm, ProjectFilterForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
def all_projects(request):
    projects = Projects.objects.all()

    if request.method == 'GET':
        form = ProjectFilterForm(request.GET)
        if form.is_valid():
            date_filter = form.cleaned_data.get('date')
            stack_filter = form.cleaned_data.get('stack')
            type_filter = form.cleaned_data.get('type')

            if date_filter == 'recent':
                projects = projects.order_by('-date_t')
            elif date_filter == 'old':
                projects = projects.order_by('date_t')

            if stack_filter:
                projects = projects.filter(stack__icontains=stack_filter)

            if type_filter:
                projects = projects.filter(type=type_filter)

    else:
        form = ProjectFilterForm()

    context = {
        'projects': projects,
        'form': form
    }
    return render(request, 'projects/all_projects.html', context)

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