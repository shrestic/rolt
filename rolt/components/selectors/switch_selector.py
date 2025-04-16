from rolt.brand.models import Brand
from rolt.common.utils import get_object
from rolt.component_types.models import ComponentType
from rolt.components.filters import SwitchFilter
from rolt.components.models.switch_model import Switch


def switch_list(filters=None) -> list[Switch]:
    filters = filters or {}
    qs = Switch.objects.select_related("brand", "type").all()
    return SwitchFilter(filters, qs).qs


def switch_get(*, code: str) -> Switch:
    qs = Switch.objects.select_related("brand", "type")
    return get_object(qs, code=code)


def switch_check_type_and_brand(
    *,
    brand: Brand,
    type: ComponentType,  # noqa: A002
) -> bool:
    return Switch.objects.filter(brand=brand, type=type).exists()
