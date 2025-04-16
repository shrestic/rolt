from typing import Any

from rolt.brand.models import Brand
from rolt.common.services import model_update
from rolt.component_types.models import ComponentType
from rolt.components.models.switch_model import Switch


def switch_create(  # noqa: PLR0913
    *,
    code: str,
    label: str,
    brand: Brand,
    is_lubed: bool,
    type: ComponentType,  # noqa: A002
    description: str,
    price: float,
    image: Any,
) -> Switch:
    return Switch.objects.create(
        code=code,
        label=label,
        brand=brand,
        is_lubed=is_lubed,
        type=type,
        description=description,
        price=price,
        image=image,
    )


def switch_bulk_create(
    *,
    switches: list[Switch],
) -> list[Switch]:
    return Switch.objects.bulk_create(switches)


def switch_update(*, instance: Switch, data: dict) -> Switch:
    fields = [
        "label",
        "brand",
        "type",
        "is_lubed",
        "description",
        "price",
        "image",
    ]
    switch, has_updated = model_update(instance=instance, fields=fields, data=data)
    return switch


def switch_delete(*, instance: Switch) -> None:
    instance.delete()
