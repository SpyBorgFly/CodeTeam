from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, EditProfileView, user_projects
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),  # Измените маршрут для профиля
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/projects/', views.user_projects, name='user_projects')
] 


