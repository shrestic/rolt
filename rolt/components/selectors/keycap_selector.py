from rolt.components.filters import KeycapFilter
from rolt.components.models.keycap_model import Keycap


def keycap_list(filters=None) -> list[Keycap]:
    filters = filters or {}
    qs = Keycap.objects.select_related("manufacturer").all().order_by("name")
    return KeycapFilter(filters, qs).qs


def keycap_get(*, code: str) -> Keycap:
    return Keycap.objects.select_related("manufacturer").filter(code=code).first()


def keycap_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Keycap.objects.filter(code__in=codes).values_list("code", flat=True),
    )
