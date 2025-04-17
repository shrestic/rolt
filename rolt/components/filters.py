from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import NumberFilter

from rolt.components.models.case_model import Case
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.stabilizer_model import Stabilizer
from rolt.components.models.switch_model import Switch


class SwitchFilter(FilterSet):
    label = CharFilter(field_name="label", lookup_expr="icontains")
    brand = CharFilter(field_name="brand__label", lookup_expr="icontains")
    brand_code = CharFilter(field_name="brand__code", lookup_expr="icontains")
    type = CharFilter(field_name="type__label", lookup_expr="icontains")
    type_code = CharFilter(field_name="type__code", lookup_expr="icontains")
    is_lubed = BooleanFilter(field_name="is_lubed")
    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Switch
        fields = [
            "label",
            "brand",
            "brand_code",
            "type",
            "type_code",
            "is_lubed",
            "price_min",
            "price_max",
        ]


class StabilizerFilter(FilterSet):
    label = CharFilter(field_name="label", lookup_expr="icontains")
    brand = CharFilter(field_name="brand__label", lookup_expr="icontains")
    brand_code = CharFilter(field_name="brand__code", lookup_expr="icontains")
    mount = CharFilter(field_name="mount__label", lookup_expr="icontains")
    mount_code = CharFilter(field_name="mount__code", lookup_expr="icontains")
    is_lubed = BooleanFilter(field_name="is_lubed")
    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Stabilizer
        fields = [
            "label",
            "brand",
            "brand_code",
            "mount",
            "mount_code",
            "is_lubed",
            "price_min",
            "price_max",
        ]


class KeycapFilter(FilterSet):
    label = CharFilter(field_name="label", lookup_expr="icontains")
    brand = CharFilter(field_name="brand__label", lookup_expr="icontains")
    brand_code = CharFilter(field_name="brand__code", lookup_expr="icontains")
    material = CharFilter(field_name="material__label", lookup_expr="icontains")
    material_code = CharFilter(field_name="material__code", lookup_expr="icontains")
    profile = CharFilter(field_name="profile__label", lookup_expr="icontains")
    profile_code = CharFilter(field_name="profile__code", lookup_expr="icontains")
    theme = CharFilter(field_name="theme", lookup_expr="icontains")

    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Keycap
        fields = [
            "label",
            "brand",
            "brand_code",
            "material",
            "material_code",
            "profile",
            "profile_code",
            "theme",
            "price_min",
            "price_max",
        ]


class CaseFilter(FilterSet):
    label = CharFilter(field_name="label", lookup_expr="icontains")
    brand = CharFilter(field_name="brand__label", lookup_expr="icontains")
    brand_code = CharFilter(field_name="brand__code", lookup_expr="icontains")
    material = CharFilter(field_name="material__label", lookup_expr="icontains")
    material_code = CharFilter(field_name="material__code", lookup_expr="icontains")
    mount_style = CharFilter(field_name="mount_style__label", lookup_expr="icontains")
    mount_style_code = CharFilter(
        field_name="mount_style__code",
        lookup_expr="icontains",
    )
    color = CharFilter(field_name="color", lookup_expr="icontains")

    price_min = NumberFilter(field_name="price", lookup_expr="gte")
    price_max = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Case
        fields = [
            "label",
            "brand",
            "brand_code",
            "material",
            "material_code",
            "mount_style",
            "mount_style_code",
            "color",
            "price_min",
            "price_max",
        ]
