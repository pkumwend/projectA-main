from django.urls import path

from .views import (
    ForgotPasswordView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
    ResetPasswordView,
)

app_name = "recovery"

urlpatterns = [
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("email-sent/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "reset-complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
