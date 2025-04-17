from rolt.brand.models import Brand
from rolt.common.utils import get_object
from rolt.component_types.models import ComponentType
from rolt.components.filters import CaseFilter
from rolt.components.models.case_model import Case


def case_list(filters=None) -> list[Case]:
    filters = filters or {}
    qs = Case.objects.select_related("brand", "material", "mount_style").all()
    return CaseFilter(filters, qs).qs


def case_get(*, code: str) -> Case:
    qs = Case.objects.select_related("brand", "material", "mount_style")
    return get_object(qs, code=code)


def case_check_material_and_mount_style_and_brand(
    *,
    brand: Brand,
    material: ComponentType,
    mount_style: ComponentType,
) -> bool:
    return Case.objects.filter(
        brand=brand,
        material=material,
        mount_style=mount_style,
    ).exists()
