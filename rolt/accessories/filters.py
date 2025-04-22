from django_filters import rest_framework as filters

from rolt.accessories.models import Accessory


class AccessoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")

    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Accessory
        fields = [
            "name",
            "type",
            "price_min",
            "price_max",
        ]
