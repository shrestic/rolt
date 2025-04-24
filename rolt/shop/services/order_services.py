import decimal

from django.db import transaction
from django.db.models import QuerySet

from rolt.accounts.models.customer_model import Customer
from rolt.shop.models.cart_model import CartItem
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem
from rolt.shop.utils import get_product_price


def order_create(*, customer: Customer, cart_items: QuerySet[CartItem]) -> Order:
    with transaction.atomic():
        order = Order.objects.create(customer=customer)

        total = decimal.Decimal("0.00")

        for item in cart_items:
            product = item.product
            if not product:
                msg = "Product not found for cart item."
                raise ValueError(msg)
            name = getattr(product, "name", "Unknown")
            if not name:
                msg = "Product name not found for cart item."
                raise ValueError(msg)
            price = get_product_price(product)
            if price is None:
                msg = "Product price not found for cart item."
                raise ValueError(msg)
            if item.quantity <= 0:
                msg = "Product quantity must be greater than zero."
                raise ValueError(msg)

            OrderItem.objects.create(
                order=order,
                content_type=item.content_type,
                object_id=item.object_id,
                name_snapshot=name,
                price_snapshot=price,
                quantity=item.quantity,
            )

            total += price * item.quantity

        order.total_amount = total
        order.save()
        cart_items.delete()

    return order


def order_update_status(
    *,
    order: Order,
    status: Order.StatusChoices,
) -> Order:
    with transaction.atomic():
        order.status = status
        order.save(update_fields=["status"])
        order.refresh_from_db()

    return order
