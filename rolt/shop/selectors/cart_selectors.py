from rolt.shop.models.cart_model import Cart


def cart_get(*, customer):
    return Cart.objects.filter(customer=customer).select_related("content_type")


def cart_exist(*, customer):
    return Cart.objects.filter(customer=customer).exists()
