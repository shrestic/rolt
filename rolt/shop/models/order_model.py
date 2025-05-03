import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from rolt.accounts.models.customer_model import Customer
from rolt.common.models import BaseModel


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "order"

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    product = GenericForeignKey("content_type", "object_id")

    name_snapshot = models.CharField(max_length=255)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        db_table = "order_item"

    def __str__(self):
        return f"OrderItem {self.id} - {self.name_snapshot} (x{self.quantity})"
