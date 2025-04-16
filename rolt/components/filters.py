from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import NumberFilter

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
