from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import FilterSet
from django_filters import UUIDFilter

from rolt.accounts.models.customer_model import Customer


class CustomerFilter(FilterSet):
    is_staff = BooleanFilter(field_name="user__is_staff")
    is_active = BooleanFilter(field_name="user__is_active")
    id = UUIDFilter(field_name="id")
    first_name = CharFilter(field_name="user__first_name", lookup_expr="icontains")
    last_name = CharFilter(field_name="user__last_name", lookup_expr="icontains")
    email = CharFilter(field_name="user__email", lookup_expr="icontains")

    birth_date_after = DateFilter(field_name="birth_date", lookup_expr="gte")
    birth_date_before = DateFilter(field_name="birth_date", lookup_expr="lte")
    phone = CharFilter(lookup_expr="icontains")
    address = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Customer
        fields = [
            "id",
            "phone",
            "address",
            "birth_date_after",
            "birth_date_before",
            "first_name",
            "last_name",
            "email",
        ]
