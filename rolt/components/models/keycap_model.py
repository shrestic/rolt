from django.db import models

from rolt.brand.models import Brand
from rolt.common.models import BaseModel
from rolt.component_types.models import ComponentType


class Keycap(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="keycap_material",
    )
    profile = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="keycap_profile",
    )
    theme = models.CharField(max_length=100, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="keycaps/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.label} - {self.brand.label}"

    class Meta:
        ordering = ["code"]
        verbose_name = "Keycap"
        verbose_name_plural = "Keycaps"
        db_table = "keycap"
