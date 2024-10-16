
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('projects/', include('projects.urls')),
    path('user/', include('accounts.urls'))
]
