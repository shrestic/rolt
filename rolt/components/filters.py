from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import NumberFilter

from rolt.components.models.kit_model import Kit


class KitFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    layout = CharFilter(field_name="layout", lookup_expr="icontains")
    layout_detail = CharFilter(field_name="layout_detail", lookup_expr="icontains")
    case_spec = CharFilter(field_name="case_spec", lookup_expr="icontains")
    mounting_style = CharFilter(field_name="mounting_style", lookup_expr="icontains")
    plate_material = CharFilter(field_name="plate_material", lookup_expr="icontains")
    stab_mount = CharFilter(field_name="stab_mount", lookup_expr="icontains")
    firmware_type = CharFilter(field_name="firmware_type", lookup_expr="icontains")
    connectivity = CharFilter(field_name="connectivity", lookup_expr="icontains")
    rgb_type = CharFilter(field_name="rgb_type", lookup_expr="icontains")

    manufacturer = CharFilter(field_name="manufacturer__label", lookup_expr="icontains")
    manufacturer_code = CharFilter(
        field_name="manufacturer__code",
        lookup_expr="icontains",
    )

    hot_swap = BooleanFilter(field_name="hot_swap")
    knob = BooleanFilter(field_name="knob")

    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Kit
        fields = [
            "name",
            "layout",
            "layout_detail",
            "case_spec",
            "mounting_style",
            "plate_material",
            "stab_mount",
            "firmware_type",
            "connectivity",
            "rgb_type",
            "manufacturer",
            "manufacturer_code",
            "hot_swap",
            "knob",
            "price_min",
            "price_max",
        ]
