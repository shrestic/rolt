from typing import Any

from rolt.brand.models import Brand
from rolt.common.services import model_update
from rolt.common.utils import get_object


# =======Brand Service=======#
def brand_create(
    *,
    code: str,
    label: str,
    logo: Any,
) -> Brand:
    return Brand.objects.create(
        code=code,
        label=label,
        logo=logo,
    )


def brand_bulk_create(
    *,
    data: list[dict],
) -> list[Brand]:
    brands = [
        Brand(
            code=item["code"],
            label=item["label"],
            logo=item["logo"],
        )
        for item in data
    ]
    return Brand.objects.bulk_create(brands)


def brand_update(*, instance: Brand, data: dict) -> Brand:
    fields = [
        "label",
        "logo",
    ]
    brand, has_updated = model_update(instance=instance, data=data, fields=fields)
    return brand


def brand_delete(*, instance: Brand) -> None:
    instance.delete()


# =======Brand Selector=======#
def brand_get(*, code: str) -> Brand | None:
    return get_object(Brand, code=code)


def brand_list() -> list[Brand]:
    return Brand.objects.all()


def brand_get_dict_by_codes(codes: list[str]) -> dict[str, Brand]:
    return Brand.objects.in_bulk(codes, field_name="code")
