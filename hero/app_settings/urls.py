from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_device/", include("apis.api_device.urls", namespace="api_device")),
    path("api_frontend/", include("apis.api_frontend.urls", namespace="api_frontend")),
]
