import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from rolt.accounts.models.customer_model import Customer
from rolt.common.models import BaseModel


class Cart(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    product = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "content_type", "object_id"],
                name="unique_customer_product_cart",
            ),
        ]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.customer} - {self.product} x{self.quantity}"
