import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from rolt.shop.models import Order
from rolt.warranty.services import warranty_create

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def activate_warranties_for_delivered_orders(sender, instance, **kwargs):
    """
    Signal to create warranties for all OrderItems when Order status is DELIVERED.
    """
    order: Order = instance
    if order.status == Order.StatusChoices.DELIVERED:
        try:
            warranty_create(order=order)
            logger.info(
                "Warranties created for Order %(order_id)s",
                extra={"order_id": order.id},
            )
        except Exception as e:
            logger.exception(
                "Failed to create warranties for Order %(order_id)s: %(error_message)s",
                extra={"order_id": order.id, "error_message": str(e)},
            )
