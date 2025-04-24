from django.urls import include
from django.urls import path

from rolt.shop.apis.cart_apis import CartClearApi
from rolt.shop.apis.cart_apis import CartCreateUpdateApi
from rolt.shop.apis.cart_apis import CartDeleteApi
from rolt.shop.apis.cart_apis import CartDetailApi

cart_patterns = [
    path("", CartDetailApi.as_view(), name="cart-detail"),
    path("create/", CartCreateUpdateApi.as_view(), name="cart-create-update"),
    path("<uuid:pk>/delete/", CartDeleteApi.as_view(), name="cart-delete"),
    path("clear/", CartClearApi.as_view(), name="cart-clear"),
]
urlpatterns = [
    path("cart/", include(cart_patterns)),
]
