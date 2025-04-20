from dataclasses import dataclass
from typing import Any

from rolt.common.services import model_update
from rolt.components.models.keycap_model import Keycap
from rolt.manufacturers.models import Manufacturer


@dataclass
class KeycapData:
    code: str
    name: str
    manufacturer: Manufacturer
    material: str
    profile: str
    legend_type: str
    shine_through: bool
    compatibility: str
    number_of_keys: int
    layout_support: str
    colorway: str
    theme_name: str
    thickness: float
    texture: str
    sound_profile: str
    image: Any
    price: int


def keycap_create(*, data: KeycapData) -> Keycap:
    return Keycap.objects.create(**data.__dict__)


def keycap_update(*, instance: Keycap, data: dict) -> Keycap:
    fields = [
        "manufacturer",
        "name",
        "material",
        "profile",
        "legend_type",
        "shine_through",
        "compatibility",
        "number_of_keys",
        "layout_support",
        "colorway",
        "theme_name",
        "thickness",
        "texture",
        "sound_profile",
        "image",
        "price",
    ]
    keycap, _ = model_update(instance=instance, fields=fields, data=data)
    return keycap


def keycap_bulk_create(*, keycaps: list[Keycap]) -> list[Keycap]:
    return Keycap.objects.bulk_create(keycaps)


def keycap_delete(*, instance: Keycap) -> None:
    instance.delete()
