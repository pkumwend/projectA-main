from django.urls import path
from . import views


urlpatterns = [
    ######################staff and admin###################################
    path(
        "staff/login/",
        views.staff_login,
        name="staff_login"
    ),

    path(
        "staff/logout/",
        views.staff_logout,
        name="staff_logout"
    ),

    path(
        "dashboard/admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "dashboard/staff/",
        views.staff_dashboard,
        name="staff_dashboard"
    ),
    ######################sessionns###########################################
    path("dashboard/sessions/",
        views.manage_sessions,
        name="manage_sessions"),
    path("dashboard/sessions/create/",
        views.create_session,
        name="create_session"),
    path("dashboard/manage/sessions/edit/<int:Session_id>/",
         views.edit_hunt,
         name="edit_session"),

    path("dashboard/manange/sessions/details/<int:Session_id>/",
    views.session_detail,
    name="session_detail"),

    path("dashboard/manage/sessions/delete/<int:Session_id>/",
         views.delete_hunt,
         name="delete_sesssion"),

    ########################hunts#############################################
    path("dashboard/manage/hunts/",
        views.manage_hunts,
        name="manage_hunts"),
 
    path("dashboard/manage/hunts/create/",
        views.create_hunt,
        name="create_hunt"),
    #adding path <int:hunt_id> is to load a page that references the scavenger hunt from dataabse to edit
    path("dashboard/manage/hunts/edit/<int:hunt_id>/",
         views.edit_hunt,
         name="edit_hunt"),
    path("dashboard/manage/hunts/delete/<int:hunt_id>/",
         views.delete_hunt,
         name="delete_hunt"),
    #####################questions############################################
    path("dashboard/questions/delete/<int:question_id>/",
        views.delete_question,
        name="delete_question"),
    path("dashboard/questions/create/",
        views.create_question,
        name="create_question"),
    path("dashboard/questions/edit/<int:question_id>/",
            views.edit_question,
            name="edit_question"),
    path("dashboard/questions/",
        views.question_pool,
        name="question_pool"),
]