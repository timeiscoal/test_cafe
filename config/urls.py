from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menus/', include("menus.urls")),
    path('users/', include("users.urls")),
]
