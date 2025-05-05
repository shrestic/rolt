from django.apps import AppConfig


class WarrantyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rolt.warranty"

    def ready(self):
        import rolt.warranty.signals  # noqa: F401
