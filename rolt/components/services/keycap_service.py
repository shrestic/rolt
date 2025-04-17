from typing import Any

from rolt.brand.models import Brand
from rolt.common.services import model_update
from rolt.component_types.models import ComponentType
from rolt.components.models.keycap_model import Keycap


def keycap_create(  # noqa: PLR0913
    *,
    code: str,
    label: str,
    brand: Brand,
    material: ComponentType,
    profile: ComponentType,
    theme: str,
    price: float,
    image: Any,
    description: str,
) -> Keycap:
    return Keycap.objects.create(
        code=code,
        label=label,
        brand=brand,
        material=material,
        profile=profile,
        theme=theme,
        price=price,
        image=image,
        description=description,
    )


def keycap_bulk_create(
    *,
    keycaps: list[Keycap],
) -> list[Keycap]:
    return Keycap.objects.bulk_create(keycaps)


def keycap_update(*, instance: Keycap, data: dict) -> Keycap:
    fields = [
        "label",
        "brand",
        "material",
        "profile",
        "theme",
        "price",
        "image",
        "description",
    ]
    keycap, has_updated = model_update(instance=instance, fields=fields, data=data)
    return keycap


def keycap_delete(*, instance: Keycap) -> None:
    instance.delete()
