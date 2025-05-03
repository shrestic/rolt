from django.urls import include
from django.urls import path

from rolt.shop.apis.cart_apis import CartClearApi
from rolt.shop.apis.cart_apis import CartItemCreateUpdateApi
from rolt.shop.apis.cart_apis import CartItemDeleteApi
from rolt.shop.apis.cart_apis import CartItemListApi
from rolt.shop.apis.order_apis import OrderCreateApi
from rolt.shop.apis.order_apis import OrderDetailApi
from rolt.shop.apis.order_apis import OrderListApi
from rolt.shop.apis.order_apis import OrderStatusUpdateApi
from rolt.shop.apis.payment_apis import PaymentCreateApi
from rolt.shop.apis.payment_apis import PaymentIPNApi
from rolt.shop.apis.payment_apis import PaymentReturnApi
from rolt.shop.apis.payment_apis import PaymentTransactionDetailApi
from rolt.shop.apis.payment_apis import PaymentTransactionListApi

cart_patterns = [
    path("", CartItemListApi.as_view(), name="cart-detail"),
    path(
        "cart-item/create/",
        CartItemCreateUpdateApi.as_view(),
        name="cart-create-update",
    ),
    path(
        "cart-item/<uuid:pk>/delete/",
        CartItemDeleteApi.as_view(),
        name="cart-delete",
    ),
    path("clear/", CartClearApi.as_view(), name="cart-clear"),
]


order_patterns = [
    path("", OrderListApi.as_view(), name="order-list"),
    path("create/", OrderCreateApi.as_view(), name="order-create"),
    path("<uuid:pk>/", OrderDetailApi.as_view(), name="order-detail"),
    path(
        "<uuid:pk>/update-status/",
        OrderStatusUpdateApi.as_view(),
        name="order-status-update",
    ),
]

payment_patterns = [
    path("return/", PaymentReturnApi.as_view(), name="payment-transaction-return"),
    path("ipn", PaymentIPNApi.as_view(), name="payment-transaction-ipn"),
    path("", PaymentTransactionListApi.as_view(), name="payment-transaction-list"),
    path(
        "<uuid:pk>",
        PaymentTransactionDetailApi.as_view(),
        name="payment-transaction-detail",
    ),
    path(
        "create/<uuid:order_id>",
        PaymentCreateApi.as_view(),
        name="payment-transaction-create",
    ),
]


urlpatterns = [
    path("cart/", include(cart_patterns)),
    path("order/", include(order_patterns)),
    path("payment/", include(payment_patterns)),
]
