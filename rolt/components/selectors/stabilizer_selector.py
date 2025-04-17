from rolt.brand.models import Brand
from rolt.common.utils import get_object
from rolt.component_types.models import ComponentType
from rolt.components.filters import StabilizerFilter
from rolt.components.models.stabilizer_model import Stabilizer


def stabilizer_list(filters=None) -> list[Stabilizer]:
    filters = filters or {}
    qs = Stabilizer.objects.select_related("brand", "mount").all()
    return StabilizerFilter(filters, qs).qs


def stabilizer_get(*, code: str) -> Stabilizer:
    qs = Stabilizer.objects.select_related("brand", "mount")
    return get_object(qs, code=code)


def stabilizer_check_mount_and_brand(
    *,
    brand: Brand,
    mount: ComponentType,
) -> bool:
    return Stabilizer.objects.filter(
        brand=brand,
        mount=mount,
    ).exists()
