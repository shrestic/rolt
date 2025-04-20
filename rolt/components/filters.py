from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import NumberFilter

from rolt.components.models.keycap_model import Keycap
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


class KeycapFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    material = CharFilter(field_name="material", lookup_expr="icontains")
    profile = CharFilter(field_name="profile", lookup_expr="icontains")
    legend_type = CharFilter(field_name="legend_type", lookup_expr="icontains")
    compatibility = CharFilter(field_name="compatibility", lookup_expr="icontains")
    layout_support = CharFilter(field_name="layout_support", lookup_expr="icontains")
    colorway = CharFilter(field_name="colorway", lookup_expr="icontains")
    theme_name = CharFilter(field_name="theme_name", lookup_expr="icontains")
    texture = CharFilter(field_name="texture", lookup_expr="icontains")
    sound_profile = CharFilter(field_name="sound_profile", lookup_expr="icontains")

    manufacturer = CharFilter(field_name="manufacturer__label", lookup_expr="icontains")
    manufacturer_code = CharFilter(
        field_name="manufacturer__code",
        lookup_expr="icontains",
    )

    shine_through = BooleanFilter(field_name="shine_through")

    number_of_keys_min = NumberFilter(field_name="number_of_keys", lookup_expr="gte")
    number_of_keys_max = NumberFilter(field_name="number_of_keys", lookup_expr="lte")

    thickness_min = NumberFilter(field_name="thickness", lookup_expr="gte")
    thickness_max = NumberFilter(field_name="thickness", lookup_expr="lte")

    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Keycap
        fields = [
            "name",
            "material",
            "profile",
            "legend_type",
            "shine_through",
            "compatibility",
            "layout_support",
            "colorway",
            "theme_name",
            "texture",
            "sound_profile",
            "manufacturer",
            "manufacturer_code",
            "number_of_keys_min",
            "number_of_keys_max",
            "thickness_min",
            "thickness_max",
            "price_min",
            "price_max",
        ]
