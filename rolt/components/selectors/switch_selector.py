from rolt.components.filters import SwitchFilter
from rolt.components.models.switch_model import Switch


def switch_list(filters=None) -> list[Switch]:
    filters = filters or {}
    qs = Switch.objects.select_related("manufacturer").all().order_by("name")
    return SwitchFilter(filters, qs).qs


def switch_get(*, code: str) -> Switch:
    return Switch.objects.select_related("manufacturer").filter(code=code).first()


def switch_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Switch.objects.filter(code__in=codes).values_list("code", flat=True),
    )
