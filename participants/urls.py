from django.urls import path

from . import views

urlpatterns = [
    path("", views.participants, name="participants"),
    path("<int:participant_id>", views.participant, name="participant")
    # It is possible to use regexes here
]