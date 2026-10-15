from django.contrib import admin
from django.urls import include, path

 
urlpatterns = [
    path("admin/", admin.site.urls),
    # Password recovery URLs use the shared templates/recovery/ directory.
    path("staff/recovery/", include("recovery.urls")),
    path("",include("home.urls")),
    path("",include("huntSessions.urls"))
]