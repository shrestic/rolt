import uuid

from django.db import models

from rolt.common.models import BaseModel
from rolt.core.validators import validate_file_size


class Accessory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=100,
    )
    description = models.TextField(blank=True, default="")
    image = models.ImageField(
        upload_to="accessories/",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    price = models.DecimalField(max_digits=14, decimal_places=0)

    class Meta:
        db_table = "accessory"
        ordering = ["name"]
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

    def __str__(self):
        return self.name
