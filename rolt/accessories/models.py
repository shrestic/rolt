from django.db import models

from rolt.common.models import BaseModel


class Accessory(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=100,
    )  # e.g., cable, wrist rest, artisan cap, etc.
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="accessories/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "accessory"
        ordering = ["name"]
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

    def __str__(self):
        return self.name
