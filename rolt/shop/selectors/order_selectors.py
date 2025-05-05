import uuid

from rolt.accounts.models.customer_model import Customer
from rolt.common.utils import get_object
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem


def order_list_by_customer(*, customer: Customer):
    return Order.objects.filter(customer=customer).order_by("-created_at")


def order_get(*, id: uuid.UUID, customer: Customer):  # noqa: A002
    return Order.objects.filter(id=id, customer=customer).first()


def orderitem_get(*, id: uuid.UUID, orderitem: OrderItem):  # noqa: A002
    return get_object(OrderItem, id=id)
