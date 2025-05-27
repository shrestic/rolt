import uuid

from django.db import models

from rolt.accessories.models import Accessory
from rolt.common.models import BaseModel
from rolt.components.models.artisan_keycap_model import ArtisanKeycap
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


class KeycapInventory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keycap = models.ForeignKey(
        Keycap,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "keycap_inventory"
        ordering = ["keycap__name"]
        verbose_name = "Keycap Inventory"
        verbose_name_plural = "Keycap Inventories"

    def __str__(self):
        return f"{self.keycap.name} - {self.quantity} units"


class ArtisanKeycapInventory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisankeycap = models.ForeignKey(
        ArtisanKeycap,
        on_delete=models.CASCADE,
        related_name="artisan_inventory",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "artisan_keycap_inventory"
        ordering = ["artisankeycap__name"]
        verbose_name = "Artisan Keycap Inventory"
        verbose_name_plural = "Artisan Keycap Inventories"

    def __str__(self):
        return f"{self.artisankeycap.name} - {self.quantity} units"


class KitInventory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kit = models.ForeignKey(
        Kit,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "kit_inventory"
        ordering = ["kit__name"]
        verbose_name = "Kit Inventory"
        verbose_name_plural = "Kit Inventories"

    def __str__(self):
        return f"{self.kit.name} - {self.quantity} units"


class SwitchInventory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    switch = models.ForeignKey(
        Switch,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "switch_inventory"
        ordering = ["switch__name"]
        verbose_name = "Switch Inventory"
        verbose_name_plural = "Switch Inventories"

    def __str__(self):
        return f"{self.switch.name} - {self.quantity} units"


class AccessoryInventory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "accessory_inventory"
        ordering = ["accessory__name"]
        verbose_name = "Accessory Inventory"
        verbose_name_plural = "Accessory Inventories"

    def __str__(self):
        return f"{self.accessory.name} - {self.quantity} units"
