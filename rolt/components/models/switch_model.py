import uuid

from django.db import models

from rolt.common.models import BaseModel
from rolt.core.validators import validate_file_size
from rolt.manufacturers.models import Manufacturer


class Switch(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="switches",
    )
    type = models.CharField(max_length=100)

    actuation_force = models.PositiveIntegerField()
    bottom_out_force = models.PositiveIntegerField()
    pre_travel = models.FloatField()
    total_travel = models.FloatField()

    sound_level = models.CharField(max_length=100)
    factory_lubed = models.BooleanField(default=False)

    stem_material = models.CharField(max_length=100)
    housing_material = models.CharField(max_length=100)

    pin_type = models.CharField(max_length=50)

    led_support = models.BooleanField(default=False)
    led_position = models.CharField(max_length=100)

    lifespan = models.PositiveIntegerField()
    compatible_with = models.CharField(max_length=255)

    image = models.ImageField(
        upload_to="switches/",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    price_per_switch = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "switch"
        ordering = ["name"]
        verbose_name = "Switch"
        verbose_name_plural = "Switches"

    def __str__(self):
        return self.name
