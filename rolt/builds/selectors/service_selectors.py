from django.core.cache import cache
from django.db.models import QuerySet

from rolt.builds.models import Service


def service_list_by_codes(
    *,
    codes: list[str],
) -> QuerySet[Service]:
    return Service.objects.filter(code__in=codes)


def service_list() -> QuerySet[Service]:
    cache_key = "service_list"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    qs = Service.objects.all()
    cache.set(cache_key, qs, timeout=1800)
    return qs
    # Cache the result for 30 minutes


def service_get_by_code(
    *,
    code: str,
) -> Service | None:
    return Service.objects.filter(code=code).first()
