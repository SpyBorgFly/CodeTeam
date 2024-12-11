from django.urls import path
from .views import (
    all_projects,
    ProjectsDetailView,
    add_comment,
    add_reply,
    add_projects,
    upload_image,
    ProjectUpdateView,
    ProjectSettingsView,
    apply_to_project,
    accept_application,
    reject_application,
    remove_participant,
    leave_project,
    delete_project,
    update_star_count
)

urlpatterns = [
    path('', all_projects, name='all_projects'),
    path('project/<int:pk>/', ProjectsDetailView.as_view(), name='project-details'),
    path('project/<int:pk>/comment/', add_comment, name='add_comment'),
    path('project/<int:pk>/reply/<int:comment_pk>/', add_reply, name='add_reply'),
    path('project/add/', add_projects, name='add_projects'),  # Правильный URL для добавления проекта
    path('project/upload-image/', upload_image, name='upload_image'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit_project'),
    path('project/<int:pk>/settings/', ProjectSettingsView.as_view(), name='project-settings'),
    path('project/<int:pk>/apply/', apply_to_project, name='apply_to_project'),
    path('project/<int:pk>/application/<int:app_id>/accept/', accept_application, name='accept_application'),
    path('project/<int:pk>/application/<int:app_id>/reject/', reject_application, name='reject_application'),
    path('project/<int:project_id>/remove-participant/<int:user_id>/', remove_participant, name='remove_participant'),
    path('project/<int:project_id>/leave/', leave_project, name='leave_project'),
    path('project/<int:pk>/delete/', delete_project, name='delete_project'),
    path('project/<int:project_id>/update-star-count/', update_star_count, name='update_star_count'),
]