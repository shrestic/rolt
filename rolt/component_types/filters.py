from django_filters import CharFilter
from django_filters import FilterSet

from rolt.component_types.models import ComponentType


class ComponentTypeFilter(FilterSet):
    code = CharFilter(lookup_expr="icontains")
    label = CharFilter(lookup_expr="icontains")
    applies_to = CharFilter(lookup_expr="icontains")
    note = CharFilter(lookup_expr="icontains")

    class Meta:
        model = ComponentType
        fields = [
            "code",
            "label",
            "applies_to",
            "note",
        ]
