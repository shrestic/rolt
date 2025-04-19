from django.db import models

from rolt.common.models import BaseModel
from rolt.manufacturers.models import Manufacturer


class Kit(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="kits",
    )

    layout = models.CharField(max_length=50)
    number_of_keys = models.PositiveIntegerField()
    layout_detail = models.CharField(max_length=100)

    case_spec = models.CharField(max_length=100)
    mounting_style = models.CharField(max_length=50)

    plate_material = models.CharField(max_length=50)
    stab_mount = models.CharField(max_length=50)
    hot_swap = models.BooleanField(default=False)

    knob = models.BooleanField(default=False)
    rgb_type = models.CharField(max_length=100)
    firmware_type = models.CharField(max_length=100)

    connectivity = models.CharField(max_length=50)

    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to="kits/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["code"]
        verbose_name = "Kit"
        verbose_name_plural = "Kits"
        db_table = "kit"

    def __str__(self):
        return f"{self.name} ({self.layout})"
