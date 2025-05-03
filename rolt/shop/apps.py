from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rolt.shop"

    def ready(self):
        import rolt.shop.signals.handlers  # noqa: F401
