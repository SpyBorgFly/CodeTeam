from django.urls import path, include
from . import views
from .views import upload_image, ProjectUpdateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.all_projects, name='all_projects'),
    path('add_projects', views.add_projects, name='add_projects'),
    path('<int:pk>', views.ProjectsDetailView.as_view(), name='project-details'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit_project'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)