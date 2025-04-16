from djoser.email import ActivationEmail
from djoser.email import ConfirmationEmail
from djoser.email import PasswordChangedConfirmationEmail
from djoser.email import PasswordResetEmail


class CustomActivationEmail(ActivationEmail):
    template_name = "email/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        try:
            path_parts = context["url"].strip("/").split("/")
            context["uid"] = path_parts[-2]
            context["token"] = path_parts[-1]
        except Exception:  # noqa: BLE001
            context["uid"] = None
            context["token"] = None
        context["protocol"] = "https"
        context["domain"] = "frontend.rolt.com"

        return context


class CustomConfirmationEmail(ConfirmationEmail):
    template_name = "email/confirmation.html"


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        try:
            parts = context["url"].strip("/").split("/")
            context["uid"] = parts[-2]
            context["token"] = parts[-1]
        except Exception:  # noqa: BLE001
            context["uid"] = None
            context["token"] = None
        context["protocol"] = "https"
        context["domain"] = "frontend.rolt.com"

        return context


class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "email/password_changed_confirmation.html"
