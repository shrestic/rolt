import uuid

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from rolt.accounts.models.customer_model import Customer
from rolt.shop.models.cart_model import CartItem


def cart_item_create_update(customer: Customer, product: Model, quantity=1):
    content_type = ContentType.objects.get_for_model(product.__class__)
    object_id = product.id

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        content_type=content_type,
        object_id=object_id,
        defaults={"quantity": quantity},
    )
    if not created:
        cart_item.quantity = quantity
        cart_item.save()
    return cart_item


# Delete a cart item by ID
def cart_item_delete(*, id, customer):  # noqa: A002
    return CartItem.objects.filter(id=id, customer=customer).delete()


# Delete all cart items for a customer
def cart_clear(*, customer):
    return CartItem.objects.filter(customer=customer).delete()


def convert_to_product(*, product_type: str, product_id: uuid.UUID):
    try:
        model = ContentType.objects.get(model=product_type).model_class()
        return model.objects.get(id=product_id)
    except ContentType.DoesNotExist:
        msg = "Invalid product type."
        raise ValueError(msg) from None
    except model.DoesNotExist:
        msg = "Product not found."
        raise ValueError(msg) from None
