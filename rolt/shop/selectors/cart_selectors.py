from rolt.shop.models.cart_model import CartItem


def cart_item_list(*, customer):
    return CartItem.objects.filter(customer=customer).select_related("content_type")


def cart_exist(*, customer):
    return CartItem.objects.filter(customer=customer).exists()
