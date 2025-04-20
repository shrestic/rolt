from django.db import models

from rolt.common.models import BaseModel
from rolt.manufacturers.models import Manufacturer


class Keycap(BaseModel):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="keycaps",
    )

    code = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255)

    material = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)
    legend_type = models.CharField(max_length=100)
    shine_through = models.BooleanField(default=False)

    compatibility = models.CharField(max_length=255)
    number_of_keys = models.PositiveIntegerField()
    layout_support = models.CharField(max_length=100)

    colorway = models.CharField(max_length=100)
    theme_name = models.CharField(max_length=100)
    thickness = models.FloatField()
    texture = models.CharField(max_length=100)
    sound_profile = models.CharField(max_length=100)

    image = models.ImageField(upload_to="keycaps/", blank=True, null=True)
    price = models.PositiveIntegerField()

    class Meta:
        db_table = "keycap"
        ordering = ["name"]
        verbose_name = "Keycap"
        verbose_name_plural = "Keycaps"

    def __str__(self):
        return self.name
