import pytest
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from rest_framework import status

from rolt.components.models.switch_model import Switch
from rolt.shop.models.cart_model import CartItem
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem

OrderStatus = Order.StatusChoices


@pytest.mark.django_db
class TestOrderApi:
    def test_if_customer_can_create_order_from_cart_return_201_and_order_item_created(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        product = baker.make(Switch, price_per_switch=1.25)
        baker.make(
            CartItem,
            customer=customer,
            object_id=product.id,
            content_type=ContentType.objects.get_for_model(Switch),
            quantity=2,
        )

        response = api_client.post("/shop/order/create/")
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.filter(customer=customer).exists()
        assert OrderItem.objects.filter(order__customer=customer).count() == 1

    def test_if_customer_can_view_order_list_return_200_and_list_with_1_item(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        order = baker.make(Order, customer=customer)
        baker.make(OrderItem, order=order)

        response = api_client.get("/shop/order/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 1

    def test_if_customer_can_view_order_detail_return_200_and_items_included(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        order = baker.make(Order, customer=customer)
        item = baker.make(OrderItem, order=order)  # noqa: F841

        response = api_client.get(f"/shop/order/{order.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(order.id)
        assert len(response.data["items"]) == 1

    def test_if_customer_can_update_order_status_return_200_and_status_changed(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        order = baker.make(Order, customer=customer, status=OrderStatus.PENDING)

        response = api_client.patch(
            f"/shop/order/{order.id}/update-status/",
            data={"status": OrderStatus.CANCELLED},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == OrderStatus.CANCELLED
