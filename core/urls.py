from django.contrib import admin
from django.urls import path
from accounts.api import api  # aqui você importa a instância única

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # usa ela normalmente
]
