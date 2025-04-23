import json
from hashlib import sha256

from django.core.cache import cache

from rolt.components.filters import KitFilter
from rolt.components.models.kit_model import Kit


def kit_list(filters: dict | None = None) -> list[Kit]:
    filters = filters or {}
    cache_key = (
        "kit_list:"
        + sha256(json.dumps(filters, sort_keys=True, default=str).encode()).hexdigest()
    )

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    qs = Kit.objects.select_related("manufacturer").all().order_by("name")
    result = KitFilter(filters, qs).qs

    cache.set(cache_key, result, timeout=3600)
    return result


def kit_get(*, code: str) -> Kit:
    return Kit.objects.select_related("manufacturer").filter(code=code).first()


def kit_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Kit.objects.filter(code__in=codes).values_list("code", flat=True),
    )
