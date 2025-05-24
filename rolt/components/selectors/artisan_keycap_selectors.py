from django.core.cache import cache

from rolt.components.models.artisan_keycap_model import ArtisanKeycap


def artisan_keycap_list() -> list[ArtisanKeycap]:
    cache_key = "artisan_keycap_list"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    result = ArtisanKeycap.objects.all().order_by("-created_at")
    cache.set(cache_key, result, timeout=1800)
    return result


def artisan_keycap_get(*, code: str) -> ArtisanKeycap:
    return ArtisanKeycap.objects.filter(code=code).first()


def artisan_keycap_get_existing_codes(*, codes: list[str]) -> set[str]:
    return set(
        ArtisanKeycap.objects.filter(code__in=codes).values_list("code", flat=True),
    )
