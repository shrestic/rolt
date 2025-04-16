from rolt.common.services import model_update
from rolt.common.utils import get_object
from rolt.component_types.filters import ComponentTypeFilter
from rolt.component_types.models import ComponentType


# =======ComponentType Selector=======#
def component_type_list(filters=None) -> list[ComponentType]:
    filters = filters or {}
    qs = ComponentType.objects.all()

    return ComponentTypeFilter(filters, qs).qs


def component_type_get(*, code: str) -> ComponentType | None:
    return get_object(ComponentType, code=code)


def component_type_check_label_and_applied_to(
    *,
    label: str,
    applies_to: str,
) -> bool:
    return ComponentType.objects.filter(label=label, applies_to=applies_to).exists()


# =======ComponentType Service=======#
def component_type_create(
    *,
    code: str,
    label: str,
    applies_to: str,
    note: str,
) -> ComponentType:
    return ComponentType.objects.create(
        code=code,
        label=label,
        applies_to=applies_to,
        note=note,
    )


def component_type_update(
    *,
    instance: ComponentType,
    data: dict,
) -> ComponentType:
    fields = [
        "code",
        "label",
        "applies_to",
        "note",
    ]
    component_type, has_updated = model_update(
        instance=instance,
        data=data,
        fields=fields,
    )
    return component_type


def component_type_delete(
    *,
    instance: ComponentType,
) -> ComponentType:
    instance.delete()
    return instance


def component_type_get_dict_by_codes(codes: list[str]) -> dict[str, ComponentType]:
    return ComponentType.objects.in_bulk(codes, field_name="code")
