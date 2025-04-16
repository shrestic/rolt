from django.db import models

from rolt.common.models import BaseModel


class ComponentType(BaseModel):
    class AppliesTo(models.TextChoices):
        SWITCH = "switch", "Switch"
        KEYCAP = "keycap", "Keycap"
        CABLE = "cable", "Cable"
        FOAM = "foam", "Foam"
        PLATE = "plate", "Plate"
        CASE = "case", "Case"
        PCB = "pcb", "PCB"
        STABILIZER = "stabilizer", "Stabilizer"
        FEET = "feet", "Feet"

    code = models.CharField(max_length=50, unique=True, db_index=True)
    label = models.CharField(max_length=100)
    applies_to = models.CharField(max_length=50, choices=AppliesTo.choices)
    note = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["code"]
        verbose_name = "Component Type"
        verbose_name_plural = "Component Types"
        db_table = "component_type"

    def __str__(self):
        return f"{self.label} ({self.applies_to})"
