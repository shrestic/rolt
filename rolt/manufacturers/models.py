from django.db import models

from rolt.common.models import BaseModel
from rolt.core.validators import validate_file_size


class Manufacturer(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="manufacturers/",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )

    class Meta:
        ordering = ["code"]
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
        db_table = "manufacturer"

    def __str__(self):
        return self.label
