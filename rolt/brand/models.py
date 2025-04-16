from django.db import models

from rolt.common.models import BaseModel


class Brand(BaseModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "brand"

    def __str__(self):
        return self.label
