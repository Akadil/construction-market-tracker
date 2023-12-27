from django.urls import path

from . import views

urlpatterns = [
    path("", views.projects, name="projects"),
    path("<int:project_id>", views.project, name="project")
    # It is possible tto use regexes here
]