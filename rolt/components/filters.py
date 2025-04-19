from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import NumberFilter

from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


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


class SwitchFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    type = CharFilter(field_name="type", lookup_expr="icontains")

    sound_level = CharFilter(field_name="sound_level", lookup_expr="icontains")
    stem_material = CharFilter(field_name="stem_material", lookup_expr="icontains")
    housing_material = CharFilter(
        field_name="housing_material",
        lookup_expr="icontains",
    )
    pin_type = CharFilter(field_name="pin_type", lookup_expr="icontains")
    compatible_with = CharFilter(field_name="compatible_with", lookup_expr="icontains")

    manufacturer = CharFilter(field_name="manufacturer__label", lookup_expr="icontains")
    manufacturer_code = CharFilter(
        field_name="manufacturer__code",
        lookup_expr="icontains",
    )

    factory_lubed = BooleanFilter(field_name="factory_lubed")
    led_support = BooleanFilter(field_name="led_support")

    actuation_force_min = NumberFilter(field_name="actuation_force", lookup_expr="gte")
    actuation_force_max = NumberFilter(field_name="actuation_force", lookup_expr="lte")

    bottom_out_force_min = NumberFilter(
        field_name="bottom_out_force",
        lookup_expr="gte",
    )
    bottom_out_force_max = NumberFilter(
        field_name="bottom_out_force",
        lookup_expr="lte",
    )

    price_min = NumberFilter(field_name="price_per_switch", lookup_expr="gte")
    price_max = NumberFilter(field_name="price_per_switch", lookup_expr="lte")

    class Meta:
        model = Switch
        fields = [
            "name",
            "type",
            "sound_level",
            "stem_material",
            "housing_material",
            "pin_type",
            "compatible_with",
            "manufacturer",
            "manufacturer_code",
            "factory_lubed",
            "led_support",
            "actuation_force_min",
            "actuation_force_max",
            "bottom_out_force_min",
            "bottom_out_force_max",
            "price_min",
            "price_max",
        ]
