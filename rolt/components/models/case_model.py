from django.db import models

from rolt.brand.models import Brand
from rolt.common.models import BaseModel
from rolt.component_types.models import ComponentType


class Case(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    material = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="case_material",
    )
    mount_style = models.ForeignKey(
        ComponentType,
        on_delete=models.PROTECT,
        related_name="case_mount_style",
    )
    color = models.CharField(max_length=50, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="cases/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.label} - {self.brand.label}"

    class Meta:
        ordering = ["code"]
        verbose_name = "Case"
        verbose_name_plural = "Cases"
        db_table = "case"
