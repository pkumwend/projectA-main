from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("join/", views.join_hunt, name="join_hunt"),
    path("questions/", views.start_hunt, name="start_hunt"),
    
]
