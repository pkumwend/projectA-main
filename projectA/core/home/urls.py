from django.urls import path
from . import views
from huntSessions import views as hunt_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("join/", views.join_hunt, name="join_hunt"),
    path("start_hunt/", hunt_views.start_hunt, name="start_hunt"),
]