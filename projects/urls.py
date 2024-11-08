from django.urls import path, include
from . import views
from .views import upload_image
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.all_projects, name='all_projects'),
    path('add_projects', views.add_projects, name='add_projects'),
    path('<int:pk>', views.ProjectsDetailView.as_view(), name='project-details'),
    path('upload_image/', views.upload_image, name='upload_image')

]