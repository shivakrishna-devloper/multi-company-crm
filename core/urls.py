from django.urls import path
from core.views.auth_views import register_view, login_view
from core.views.project_views import list_projects, create_project, delete_project

urlpatterns = [
    path('auth/register/', register_view),
    path('auth/login/',    login_view),
    path('projects/',      list_projects),
    path('projects/create/', create_project),
    path('projects/<str:pid>/delete/', delete_project),
]