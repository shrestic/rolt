from django.db import models

from rolt.brand.models import Brand
from rolt.common.models import BaseModel
from rolt.component_types.models import ComponentType


class Switch(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="switch_type",
    )
    is_lubed = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="switches/", blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"{self.label} - {self.brand.label}"

    class Meta:
        ordering = ["code"]
        verbose_name = "Switch"
        verbose_name_plural = "Switches"
        db_table = "switch"
