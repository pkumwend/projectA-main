import re
from datetime import datetime, timedelta
from unittest.mock import patch
from urllib.parse import urlsplit

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    MAILERS={"default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"}},
    DEFAULT_FROM_EMAIL="no-reply@example.com",
    RECOVERY_LOGIN_URL="/staff/login/",
    PASSWORD_RESET_TIMEOUT=3600,
    AUTH_PASSWORD_VALIDATORS=[
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ],
)
class RecoveryFlowTests(TestCase):
    """Exercise real Django tokens, forms, sessions, and email templates."""

    old_password = "OldHunt!47pXq2"
    new_password = "FreshHunt!86vKt3"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user(
            username="recovery_staff",
            email="recovery.demo.staff@gmail.com",
            password=cls.old_password,
            is_staff=True,
        )
        cls.outlook_staff = User.objects.create_user(
            username="recovery_outlook",
            email="recovery.demo.staff@outlook.com",
            password=cls.old_password,
            is_staff=True,
        )
        cls.inactive = User.objects.create_user(
            username="recovery_inactive",
            email="inactive@example.com",
            password=cls.old_password,
            is_active=False,
        )
        cls.external_user = User.objects.create_user(
            username="recovery_external",
            email="external@example.com",
            password=None,
        )

    def email_reset_path(self, email=None):
        response = self.client.post(
            reverse("recovery:forgot_password"),
            {"email": email or self.staff.email},
        )
        self.assertRedirects(response, reverse("recovery:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        link = re.search(r"https?://[^\s]+", mail.outbox[0].body).group(0)
        return urlsplit(link).path

    def open_reset_form(self, client=None):
        client = client or self.client
        original_path = self.email_reset_path()
        response = client.get(original_path, follow=True)
        self.assertTrue(response.context["validlink"])
        form_path = response.request["PATH_INFO"]
        self.assertIn("/set-password/", form_path)
        return original_path, form_path

    def test_forgot_page_has_registered_email_field(self):
        response = self.client.get(reverse("recovery:forgot_password"))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'autocomplete="email"')
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "/staff/login/")

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            reverse("recovery:forgot_password"), {"email": "not-an-email"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(len(mail.outbox), 0)

    def test_gmail_receives_plain_text_and_html_button(self):
        path = self.email_reset_path()
        message = mail.outbox[0]
        self.assertEqual(message.to, [self.staff.email])
        self.assertIn("/staff/recovery/reset-password/", path)
        self.assertIn("expires in 60 minutes", message.body)
        self.assertNotIn(self.old_password, message.body)
        self.assertEqual(message.alternatives[0].mimetype, "text/html")
        self.assertIn("Confirm password reset", message.alternatives[0].content)
        self.assertIn(path, message.alternatives[0].content)

    def test_outlook_receives_the_same_reset_flow(self):
        self.email_reset_path(self.outlook_staff.email)
        self.assertEqual(mail.outbox[0].to, [self.outlook_staff.email])

    def test_unknown_email_gets_generic_page_without_sending_mail(self):
        response = self.client.post(
            reverse("recovery:forgot_password"),
            {"email": "not-registered@example.com"},
            follow=True,
        )
        self.assertContains(response, "If an active account")
        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_and_unusable_password_accounts_get_no_email(self):
        for user in (self.inactive, self.external_user):
            with self.subTest(user=user.username):
                response = self.client.post(
                    reverse("recovery:forgot_password"), {"email": user.email}
                )
                self.assertRedirects(response, reverse("recovery:password_reset_done"))
                self.assertEqual(len(mail.outbox), 0)

    def test_clicking_email_only_opens_the_form(self):
        original_path, form_path = self.open_reset_form()
        self.assertNotEqual(original_path, form_path)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password(self.old_password))

    def test_password_confirmation_must_match(self):
        _, path = self.open_reset_form()
        response = self.client.post(
            path,
            {"new_password1": self.new_password, "new_password2": "Different!35"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_password2", response.context["form"].errors)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password(self.old_password))

    def test_weak_password_is_rejected_by_django_validators(self):
        _, path = self.open_reset_form()
        response = self.client.post(
            path, {"new_password1": "123", "new_password2": "123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password(self.old_password))

    def test_success_changes_password_and_preserves_account_details(self):
        _, path = self.open_reset_form()
        response = self.client.post(
            path,
            {"new_password1": self.new_password, "new_password2": self.new_password},
            follow=True,
        )
        self.assertContains(response, "Your password has been changed successfully.")
        self.assertContains(response, "/staff/login/")
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password(self.new_password))
        self.assertFalse(self.staff.check_password(self.old_password))
        self.assertNotEqual(self.staff.password, self.new_password)
        self.assertEqual(self.staff.username, "recovery_staff")
        self.assertEqual(self.staff.email, "recovery.demo.staff@gmail.com")
        self.assertTrue(self.staff.is_staff)
        self.assertFalse(self.staff.is_superuser)
        self.assertIsNone(
            authenticate(username=self.staff.username, password=self.old_password)
        )
        self.assertIsNotNone(
            authenticate(username=self.staff.username, password=self.new_password)
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_used_link_and_form_session_cannot_reset_again(self):
        original_path, form_path = self.open_reset_form()
        self.client.post(
            form_path,
            {"new_password1": self.new_password, "new_password2": self.new_password},
        )
        for path in (original_path, form_path):
            with self.subTest(path=path):
                response = self.client.get(path, follow=True)
                self.assertFalse(response.context["validlink"])
                self.assertNotContains(response, 'name="new_password1"')

    def test_expired_link_is_rejected(self):
        with patch.object(
            default_token_generator,
            "_now",
            return_value=datetime.now() - timedelta(seconds=3601),
        ):
            token = default_token_generator.make_token(self.staff)
        path = reverse(
            "recovery:reset_password",
            kwargs={"uidb64": urlsafe_base64_encode(force_bytes(self.staff.pk)), "token": token},
        )
        response = self.client.get(path)
        self.assertFalse(response.context["validlink"])
        self.assertContains(response, "Request a new reset link")

    def test_tampered_token_is_rejected(self):
        path = self.email_reset_path()
        token = path.rstrip("/").split("/")[-1]
        tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
        response = self.client.get(path.replace(token, tampered))
        self.assertFalse(response.context["validlink"])

    def test_invalid_user_id_is_rejected(self):
        path = reverse(
            "recovery:reset_password", kwargs={"uidb64": "invalid-user", "token": "bad-token"}
        )
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["validlink"])

    def test_set_password_url_requires_the_validated_session(self):
        _, path = self.open_reset_form()
        response = Client().get(path)
        self.assertFalse(response.context["validlink"])

    def test_forgot_password_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            reverse("recovery:forgot_password"), {"email": self.staff.email}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        _, path = self.open_reset_form(client)
        response = client.post(
            path,
            {"new_password1": self.new_password, "new_password2": self.new_password},
        )
        self.assertEqual(response.status_code, 403)
        self.staff.refresh_from_db()
        self.assertTrue(self.staff.check_password(self.old_password))

    def test_email_lifetime_follows_settings(self):
        with override_settings(PASSWORD_RESET_TIMEOUT=900):
            self.email_reset_path()
        self.assertIn("expires in 15 minutes", mail.outbox[0].body)

    def test_authenticated_sessions_are_invalidated_after_reset(self):
        old_session = Client()
        old_session.force_login(self.staff)
        _, path = self.open_reset_form()
        self.client.post(
            path,
            {"new_password1": self.new_password, "new_password2": self.new_password},
        )
        response = old_session.get(reverse("recovery:forgot_password"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
