from typing import Any

from rolt.common.services import model_update
from rolt.common.utils import get_object
from rolt.manufacturers.models import Manufacturer


# =======manufacturer Service=======#
def manufacturer_create(
    *,
    code: str,
    label: str,
    logo: Any,
) -> Manufacturer:
    return Manufacturer.objects.create(
        code=code,
        label=label,
        logo=logo,
    )


def manufacturer_bulk_create(
    *,
    data: list[dict],
) -> list[Manufacturer]:
    manufacturers = [
        Manufacturer(
            code=item["code"],
            label=item["label"],
            logo=item["logo"],
        )
        for item in data
    ]
    return Manufacturer.objects.bulk_create(manufacturers)


def manufacturer_update(*, instance: Manufacturer, data: dict) -> Manufacturer:
    fields = [
        "label",
        "logo",
    ]
    manufacturer, has_updated = model_update(
        instance=instance,
        data=data,
        fields=fields,
    )
    return manufacturer


def manufacturer_delete(*, instance: Manufacturer) -> None:
    instance.delete()


# =======Manufacturer Selector=======#
def manufacturer_get(*, code: str) -> Manufacturer | None:
    return get_object(Manufacturer, code=code)


def manufacturer_list() -> list[Manufacturer]:
    return Manufacturer.objects.all()


def manufacturer_get_dict_by_codes(codes: list[str]) -> dict[str, Manufacturer]:
    return Manufacturer.objects.in_bulk(codes, field_name="code")
