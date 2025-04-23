import json
from hashlib import sha256

from django.core.cache import cache

from rolt.accessories.filters import AccessoryFilter
from rolt.accessories.models import Accessory


def accessory_list(filters: dict | None = None) -> list[Accessory]:
    filters = filters or {}
    cache_key = (
        "accessory_list:"
        + sha256(json.dumps(filters, sort_keys=True, default=str).encode()).hexdigest()
    )

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    qs = Accessory.objects.all().order_by("name")
    result = AccessoryFilter(filters, qs).qs
    cache.set(cache_key, result, timeout=1800)

    return result


def accessory_get(*, id) -> Accessory | None:  # noqa: A002
    return Accessory.objects.filter(id=id).first()
