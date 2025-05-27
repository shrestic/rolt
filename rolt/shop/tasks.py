from celery import shared_task
from django.utils import timezone

from rolt.shop.models.order_model import Order


@shared_task
def update_order_status():
    # If an order have status "pending" for more than 15 minutes, change it to "cancelled"  # noqa: E501
    fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)
    Order.objects.filter(
        status=Order.StatusChoices.PENDING,
        created_at__lt=fifteen_minutes_ago,
    ).update(status=Order.StatusChoices.CANCELLED)
    # If an order have status "paid" for more than 7 days, change it to "delivered"
    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    Order.objects.filter(
        status=Order.StatusChoices.PAID,
        created_at__lt=seven_days_ago,
    ).update(status=Order.StatusChoices.DELIVERED)
