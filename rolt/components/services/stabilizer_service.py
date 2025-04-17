from typing import Any

from rolt.brand.models import Brand
from rolt.common.services import model_update
from rolt.component_types.models import ComponentType
from rolt.components.models.stabilizer_model import Stabilizer


def stabilizer_create(  # noqa: PLR0913
    *,
    code: str,
    label: str,
    brand: Brand,
    mount: ComponentType,
    is_lubed: bool,
    price: float,
    image: Any,
    description: str,
) -> Stabilizer:
    return Stabilizer.objects.create(
        code=code,
        label=label,
        brand=brand,
        mount=mount,
        is_lubed=is_lubed,
        price=price,
        image=image,
        description=description,
    )


def stabilizer_bulk_create(
    *,
    stabilizers: list[Stabilizer],
) -> list[Stabilizer]:
    return Stabilizer.objects.bulk_create(stabilizers)


def stabilizer_update(*, instance: Stabilizer, data: dict) -> Stabilizer:
    fields = [
        "label",
        "brand",
        "mount",
        "is_lubed",
        "price",
        "image",
        "description",
    ]
    stabilizer, has_updated = model_update(instance=instance, fields=fields, data=data)
    return stabilizer


def stabilizer_delete(*, instance: Stabilizer) -> None:
    instance.delete()
