from dataclasses import dataclass
from typing import Any

from rolt.common.services import model_update
from rolt.components.cache import clear_kit_cache
from rolt.components.models.kit_model import Kit
from rolt.manufacturers.models import Manufacturer


@dataclass
class KitData:
    code: str
    name: str
    manufacturer: Manufacturer
    layout: str
    number_of_keys: int
    layout_detail: str
    case_spec: str
    mounting_style: str
    plate_material: str
    stab_mount: str
    hot_swap: bool
    knob: bool
    rgb_type: str
    firmware_type: str
    connectivity: str
    dimensions: str
    weight: float
    image: Any
    price: int


@clear_kit_cache
def kit_create(*, data: KitData) -> Kit:
    return Kit.objects.create(**data.__dict__)


@clear_kit_cache
def kit_update(*, instance: Kit, data: dict) -> Kit:
    fields = [
        "name",
        "manufacturer",
        "layout",
        "number_of_keys",
        "layout_detail",
        "case_spec",
        "mounting_style",
        "plate_material",
        "stab_mount",
        "hot_swap",
        "knob",
        "rgb_type",
        "firmware_type",
        "connectivity",
        "dimensions",
        "weight",
        "image",
        "price",
    ]
    kit, _ = model_update(instance=instance, fields=fields, data=data)
    return kit


@clear_kit_cache
def kit_bulk_create(*, kits: list[Kit]) -> list[Kit]:
    return Kit.objects.bulk_create(kits)


@clear_kit_cache
def kit_delete(*, instance: Kit) -> None:
    instance.delete()
