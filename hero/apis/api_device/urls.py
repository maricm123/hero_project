from django.urls import include, path

from .views import views_config
app_name = "api_device"

urlpatterns = [
    path(
        route="device-config/",
        view=views_config.ConfigView.as_view(),
        name="device-config",
    ),
]