import uuid

from django.db.models import QuerySet

from rolt.accounts.models.customer_model import Customer
from rolt.shop.models.order_model import OrderItem
from rolt.warranty.models import Warranty
from rolt.warranty.models import WarrantyRequest


# ----------Warranty Selectors----------#
def warranty_list_by_customer(*, customer: Customer) -> QuerySet[Warranty]:
    return (
        Warranty.objects.filter(customer=customer)
        .select_related("orderitem")
        .order_by("-start_date")
    )


def warranty_get_by_orderitem(*, orderitem: OrderItem) -> Warranty | None:
    return (
        Warranty.objects.filter(orderitem=orderitem).select_related("customer").first()
    )


def warranty_get(*, id: uuid.UUID) -> Warranty | None:  # noqa: A002
    return (
        Warranty.objects.select_related("customer", "orderitem").filter(id=id).first()
    )


# ----------WarrantyRequest Selectors----------#
def warranty_request_list_by_customer(
    *,
    customer: Customer,
) -> QuerySet[WarrantyRequest]:
    return (
        WarrantyRequest.objects.filter(customer=customer)
        .select_related("warranty", "warranty__orderitem")
        .order_by("-created_at")
    )


def warranty_request_list_all() -> QuerySet[WarrantyRequest]:  # For admin
    return WarrantyRequest.objects.select_related(
        "customer",
        "warranty",
        "warranty__orderitem",
    ).order_by("-created_at")


def warranty_request_get(*, id: uuid.UUID) -> WarrantyRequest | None:  # noqa: A002
    return (
        WarrantyRequest.objects.select_related(
            "customer",
            "warranty",
            "warranty__orderitem",
        )
        .filter(id=id)
        .first()
    )
