from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_projects, name='all_projects'),
    path('add_projects', views.add_projects, name='add_projects'),
    path('<int:pk>', views.ProjectsDetailView.as_view(), name='project-details')

]