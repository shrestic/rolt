import uuid

from django.db import models

from rolt.accounts.models.customer_model import Customer
from rolt.common.models import BaseModel
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


class Build(BaseModel):
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

    class Meta:
        db_table = "builds"
        ordering = ["-created_at"]
        verbose_name = "Build"
        verbose_name_plural = "Builds"

    def __str__(self):
        return self.name


class Showcase(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    build = models.OneToOneField(
        Build,
        on_delete=models.CASCADE,
        related_name="showcase",
        limit_choices_to={"is_preset": True},
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="build_showcases/", null=True, blank=True)

    class Meta:
        db_table = "showcase"
        ordering = ["-created_at"]
        verbose_name = "Showcase"
        verbose_name_plural = "Showcases"

    def __str__(self):
        return self.title
