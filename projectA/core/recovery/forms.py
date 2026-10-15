from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class RecoveryPasswordResetForm(PasswordResetForm):
    """Keep Django's email checks and add the recovery page's presentation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email address"
        self.fields["email"].widget.attrs.update(
            {
                "class": "recovery-input",
                "placeholder": "Enter your registered email address",
                "autocomplete": "email",
                "autofocus": True,
            }
        )


class RecoverySetPasswordForm(SetPasswordForm):
    """Keep Django's password matching, validation, hashing, and saving."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].label = "New password"
        self.fields["new_password2"].label = "Confirm new password"
        for name, placeholder in (
            ("new_password1", "Enter your new password"),
            ("new_password2", "Enter your new password again"),
        ):
            self.fields[name].widget.attrs.update(
                {
                    "class": "recovery-input",
                    "placeholder": placeholder,
                    "autocomplete": "new-password",
                }
            )
        self.fields["new_password1"].widget.attrs["autofocus"] = True
