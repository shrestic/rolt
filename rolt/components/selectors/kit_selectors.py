from rolt.components.filters import KitFilter
from rolt.components.models.kit_model import Kit


def kit_list(filters=None) -> list[Kit]:
    filters = filters or {}
    qs = Kit.objects.select_related("manufacturer").all().order_by("name")
    return KitFilter(filters, qs).qs


def kit_get(*, code: str) -> Kit:
    return Kit.objects.select_related("manufacturer").filter(code=code).first()


def kit_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Kit.objects.filter(code__in=codes).values_list("code", flat=True),
    )
