import uuid

from django.core.cache import cache
from django.db.models import QuerySet

from rolt.builds.models import Showcase


def showcase_list() -> QuerySet[Showcase]:
    cache_key = "showcase_list"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    qs = (
        Showcase.objects.select_related("build")
        .filter(build__is_preset=True)
        .order_by("-build__created_at")
    )
    cache.set(cache_key, qs, timeout=1800)  # Cache for 30 minutes
    return qs


def showcase_get(
    *,
    id: uuid.UUID,  # noqa: A002
) -> Showcase | None:
    return Showcase.objects.select_related("build").filter(id=id).first()


def showcase_get_by_build_id(
    *,
    build_id: uuid.UUID,
) -> Showcase | None:
    return Showcase.objects.select_related("build").filter(build_id=build_id).first()
