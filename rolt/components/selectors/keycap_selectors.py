import json
from hashlib import sha256

from django.core.cache import cache

from rolt.components.filters import KeycapFilter
from rolt.components.models.keycap_model import Keycap


def keycap_list(filters: dict | None = None) -> list[Keycap]:
    filters = filters or {}
    cache_key = (
        "keycap_list:"
        + sha256(json.dumps(filters, sort_keys=True, default=str).encode()).hexdigest()
    )

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    qs = Keycap.objects.select_related("manufacturer").all().order_by("name")
    result = KeycapFilter(filters, qs).qs

    cache.set(cache_key, result, timeout=1800)
    return result


def keycap_get(*, code: str) -> Keycap:
    return Keycap.objects.select_related("manufacturer").filter(code=code).first()


def keycap_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Keycap.objects.filter(code__in=codes).values_list("code", flat=True),
    )
