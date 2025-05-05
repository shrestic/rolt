import uuid

from django.db import models
from django.utils import timezone

from rolt.accounts.models.customer_model import Customer
from rolt.common.models import BaseModel
from rolt.shop.models.order_model import OrderItem


class Warranty(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    orderitem = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="warranty",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="warranties",
    )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        VOIDED = "voided", "Voided"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "warranty"
        ordering = ["-start_date"]
        verbose_name = "Warranty"
        verbose_name_plural = "Warranties"

    def __str__(self):
        return f"{self.orderitem.name_snapshot} - {self.status}"


class WarrantyRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    warranty = models.ForeignKey(
        Warranty,
        on_delete=models.CASCADE,
        related_name="requests",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="warranty_requests",
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    admin_notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "warranty_request"
        ordering = ["-created_at"]
        verbose_name = "Warranty Request"
        verbose_name_plural = "Warranty Requests"

    def __str__(self):
        return f"{self.warranty} - {self.status}"
