import uuid

from django.db import models

from rolt.common.models import BaseModel
from rolt.core.validators import validate_file_size


class ArtisanKeycap(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)

    profile = models.CharField(max_length=100)
    colorway = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="artisan_keycaps/",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=14, decimal_places=0)

    limited_quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "artisan_keycap"
        ordering = ["-created_at"]
        verbose_name = "Artisan Keycap"
        verbose_name_plural = "Artisan Keycaps"

    def __str__(self):
        return f"{self.name} by {self.artist_name}"
