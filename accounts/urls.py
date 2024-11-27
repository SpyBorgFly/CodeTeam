from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, EditProfileView, user_projects
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),  # Измените маршрут для профиля
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/projects/', views.user_projects, name='user_projects'),
    path('profile/<str:username>/projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('settings/', views.user_settings, name='user_settings'),
    path('review_applications/', views.review_applications, name='review_applications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


