from django.urls import include, path
from .views import views_config

app_name = "api_frontend"

urlpatterns = [
    path(
        route="frontend-config/",
        view=views_config.ConfigView.as_view(),
        name="frontend-config",
    ),
]