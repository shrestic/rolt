from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rolt.accounts"

    def ready(self):
        import rolt.accounts.signals.handlers  # noqa: F401
