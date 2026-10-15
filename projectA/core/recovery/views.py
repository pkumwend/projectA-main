from math import ceil

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

from .forms import RecoveryPasswordResetForm, RecoverySetPasswordForm


class RecoveryContextMixin:
    """Share the login destination without changing the existing login view."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recovery_login_url"] = resolve_url(
            getattr(settings, "RECOVERY_LOGIN_URL", "/staff/login/")
        )
        return context


class ForgotPasswordView(RecoveryContextMixin, auth_views.PasswordResetView):
    template_name = "recovery/forgot_password.html"
    form_class = RecoveryPasswordResetForm
    email_template_name = "recovery/password_reset_email.txt"
    html_email_template_name = "recovery/password_reset_email.html"
    subject_template_name = "recovery/password_reset_subject.txt"
    success_url = reverse_lazy("recovery:password_reset_done")

    def form_valid(self, form):
        # Show the actual configured lifetime in both email formats.
        self.extra_email_context = {
            **(self.extra_email_context or {}),
            "reset_timeout_minutes": ceil(settings.PASSWORD_RESET_TIMEOUT / 60),
        }
        return super().form_valid(form)


class PasswordResetDoneView(RecoveryContextMixin, auth_views.PasswordResetDoneView):
    template_name = "recovery/password_reset_done.html"


class ResetPasswordView(RecoveryContextMixin, auth_views.PasswordResetConfirmView):
    template_name = "recovery/reset_password.html"
    form_class = RecoverySetPasswordForm
    success_url = reverse_lazy("recovery:password_reset_complete")
    post_reset_login = False


class PasswordResetCompleteView(
    RecoveryContextMixin, auth_views.PasswordResetCompleteView
):
    template_name = "recovery/password_reset_complete.html"
