import json
from hashlib import sha256

from django.core.cache import cache

from rolt.components.filters import SwitchFilter
from rolt.components.models.switch_model import Switch


def switch_list(filters: dict | None = None) -> list[Switch]:
    filters = filters or {}
    cache_key = (
        "switch_list:"
        + sha256(json.dumps(filters, sort_keys=True, default=str).encode()).hexdigest()
    )

    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    qs = Switch.objects.select_related("manufacturer").all().order_by("name")
    result = SwitchFilter(filters, qs).qs
    cache.set(cache_key, result, timeout=1800)
    return result


def switch_get(*, code: str) -> Switch:
    return Switch.objects.select_related("manufacturer").filter(code=code).first()


def switch_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        Switch.objects.filter(code__in=codes).values_list("code", flat=True),
    )
