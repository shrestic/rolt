from dataclasses import dataclass
from typing import Any

from rolt.common.services import model_update
from rolt.components.cache import clear_switch_cache
from rolt.components.models.switch_model import Switch
from rolt.manufacturers.models import Manufacturer


@dataclass
class SwitchData:
    code: str
    name: str
    type: str
    manufacturer: Manufacturer
    actuation_force: int
    bottom_out_force: int
    pre_travel: float
    total_travel: float
    sound_level: str
    factory_lubed: bool
    stem_material: str
    housing_material: str
    pin_type: str
    led_support: bool
    led_position: str
    lifespan: int
    compatible_with: str
    image: Any
    price_per_switch: int
    description: str


@clear_switch_cache
def switch_create(*, data: SwitchData) -> Switch:
    return Switch.objects.create(**data.__dict__)


@clear_switch_cache
def switch_update(*, instance: Switch, data: dict) -> Switch:
    fields = [
        "manufacturer",
        "name",
        "type",
        "actuation_force",
        "bottom_out_force",
        "pre_travel",
        "total_travel",
        "sound_level",
        "factory_lubed",
        "stem_material",
        "housing_material",
        "pin_type",
        "led_support",
        "led_position",
        "lifespan",
        "compatible_with",
        "image",
        "price_per_switch",
        "description",
    ]
    switch, _ = model_update(instance=instance, fields=fields, data=data)
    return switch


@clear_switch_cache
def switch_bulk_create(*, switches: list[Switch]) -> list[Switch]:
    return Switch.objects.bulk_create(switches)


@clear_switch_cache
def switch_delete(*, instance: Switch) -> None:
    instance.delete()
