from dataclasses import dataclass
from typing import Any

from rolt.common.services import model_update
from rolt.common.utils import invalidate_cache
from rolt.components.models.artisan_keycap_model import ArtisanKeycap


@dataclass
class ArtisanKeycapData:
    name: str
    code: str
    artist_name: str
    profile: str
    colorway: str
    image: Any
    price: int
    description: str
    limited_quantity: int


@invalidate_cache(specific_key="artisan_keycap_list")
def artisan_keycap_create(*, data: ArtisanKeycapData) -> ArtisanKeycap:
    return ArtisanKeycap.objects.create(**data.__dict__)


@invalidate_cache(specific_key="artisan_keycap_list")
def artisan_keycap_update(*, instance: ArtisanKeycap, data: dict) -> ArtisanKeycap:
    fields = [
        "name",
        "code",
        "artist_name",
        "profile",
        "colorway",
        "image",
        "price",
        "description",
        "limited_quantity",
    ]
    ak, _ = model_update(instance=instance, fields=fields, data=data)
    return ak


@invalidate_cache(specific_key="artisan_keycap_list")
def artisan_keycap_bulk_create(
    *,
    artisan_keycaps: list[ArtisanKeycap],
) -> list[ArtisanKeycap]:
    return ArtisanKeycap.objects.bulk_create(artisan_keycaps)


@invalidate_cache(specific_key="artisan_keycap_list")
def artisan_keycap_delete(*, instance: ArtisanKeycap) -> None:
    instance.delete()
