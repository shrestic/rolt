from typing import Any

from rolt.brand.models import Brand
from rolt.common.services import model_update
from rolt.component_types.models import ComponentType
from rolt.components.models.case_model import Case


def case_create(  # noqa: PLR0913
    *,
    code: str,
    label: str,
    brand: Brand,
    material: ComponentType,
    mount_style: ComponentType,
    color: str,
    price: float,
    image: Any,
    description: str,
) -> Case:
    return Case.objects.create(
        code=code,
        label=label,
        brand=brand,
        material=material,
        mount_style=mount_style,
        color=color,
        price=price,
        image=image,
        description=description,
    )


def case_bulk_create(
    *,
    cases: list[Case],
) -> list[Case]:
    return Case.objects.bulk_create(cases)


def case_update(*, instance: Case, data: dict) -> Case:
    fields = [
        "label",
        "brand",
        "material",
        "mount_style",
        "color",
        "price",
        "image",
        "description",
    ]
    case, has_updated = model_update(instance=instance, fields=fields, data=data)
    return case


def case_delete(*, instance: Case) -> None:
    instance.delete()
