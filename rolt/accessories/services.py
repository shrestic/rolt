from dataclasses import dataclass
from typing import Any

from rolt.accessories.models import Accessory
from rolt.common.services import model_update


@dataclass
class AccessoryData:
    name: str
    type: str
    description: str
    image: Any
    price: float


def accessory_create(*, data: AccessoryData) -> Accessory:
    return Accessory.objects.create(**data.__dict__)


def accessory_update(*, instance: Accessory, data: dict) -> Accessory:
    fields = ["name", "type", "description", "image", "price"]
    accessory, _ = model_update(instance=instance, fields=fields, data=data)
    return accessory


def accessory_bulk_create(*, accessories: list[Accessory]) -> list[Accessory]:
    return Accessory.objects.bulk_create(accessories)


def accessory_delete(*, instance: Accessory) -> None:
    instance.delete()
