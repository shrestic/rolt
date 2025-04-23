import uuid

from django.db.models.query import QuerySet

from rolt.accounts.filters import CustomerFilter
from rolt.accounts.models.customer_model import Customer
from rolt.common.utils import get_object


class CustomerSelector:
    def __init__(self) -> None:
        pass

    def customer_get(
        self,
        *,
        pk: uuid.UUID | None = None,
        user_id: uuid.UUID | None = None,
    ) -> Customer | None:
        queryset = Customer.objects.select_related("user")
        if pk:
            return get_object(queryset, pk=pk)
        if user_id:
            return get_object(queryset, user_id=user_id)
        return None

    def customer_list(self, filters: dict | None = None) -> QuerySet[Customer]:
        filters = filters or {}

        qs = Customer.objects.select_related("user").all()

        return CustomerFilter(filters, qs).qs
