from rolt.brand.models import Brand
from rolt.common.utils import get_object
from rolt.component_types.models import ComponentType
from rolt.components.filters import KeycapFilter
from rolt.components.models.keycap_model import Keycap


def keycap_list(filters=None) -> list[Keycap]:
    filters = filters or {}
    qs = Keycap.objects.select_related("brand", "material", "profile").all()
    return KeycapFilter(filters, qs).qs


def keycap_get(*, code: str) -> Keycap:
    qs = Keycap.objects.select_related("brand", "material", "profile")
    return get_object(qs, code=code)


def keycap_check_material_and_profile_and_brand(
    *,
    brand: Brand,
    material: ComponentType,
    profile: ComponentType,
) -> bool:
    return Keycap.objects.filter(
        brand=brand,
        material=material,
        profile=profile,
    ).exists()
