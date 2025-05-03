import uuid

from django.db.models import QuerySet

from rolt.accounts.models.customer_model import Customer
from rolt.common.utils import get_object
from rolt.shop.models.payment_transaction_model import PaymentTransaction


def payment_transaction_list_by_customer(
    *,
    customer: Customer,
) -> QuerySet[PaymentTransaction]:
    return (
        PaymentTransaction.objects.select_related("order")
        .filter(order__customer=customer)
        .order_by("-created_at")
    )


def payment_transaction_get_by_txn_ref(*, txn_ref: str) -> PaymentTransaction | None:
    return get_object(PaymentTransaction, txn_ref=txn_ref)


def payment_transaction_get(
    *,
    id: uuid.UUID,  # noqa: A002
    customer: Customer,
) -> PaymentTransaction | None:
    return get_object(
        PaymentTransaction,
        id=id,
        order__customer=customer,
    )
