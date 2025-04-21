import uuid

from django.db import models

from rolt.accounts.models.customer_model import Customer
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


class Build(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name="builds",
        null=True,
        blank=True,
    )

    kit = models.ForeignKey(
        Kit,
        on_delete=models.CASCADE,
        related_name="builds",
    )
    switch = models.ForeignKey(
        Switch,
        on_delete=models.CASCADE,
        related_name="builds",
    )
    switch_quantity = models.PositiveIntegerField()
    keycap = models.ForeignKey(
        Keycap,
        on_delete=models.CASCADE,
        related_name="builds",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    is_preset = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "builds"
        ordering = ["-created_at"]
        verbose_name = "Build"
        verbose_name_plural = "Builds"

    def __str__(self):
        return self.name
