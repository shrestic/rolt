from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rolt.inventory"

    def ready(self):
        # Import signals here to avoid circular imports
        import rolt.inventory.signals.cart_handlers
        import rolt.inventory.signals.payment_handlers
        import rolt.inventory.signals.product_handlers  # noqa: F401
