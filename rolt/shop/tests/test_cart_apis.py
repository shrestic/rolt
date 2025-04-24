import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.switch_model import Switch
from rolt.shop.models.cart_model import CartItem


@pytest.mark.django_db
class TestCartApi:
    def test_if_customer_can_create_cart_item_return_201_and_item_created(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        switch = baker.make(Switch)

        payload = {
            "product_type": "switch",
            "product_id": str(switch.id),
            "quantity": 10,
        }

        response = api_client.post(
            "/shop/cart/cart-item/create/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert CartItem.objects.filter(customer=customer).exists()

    def test_if_customer_can_view_cart_items_return_200_and_list(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        product = baker.make(Switch)
        baker.make(CartItem, customer=customer, object_id=product.id)

        response = api_client.get("/shop/cart/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_if_customer_can_clear_cart_return_204_and_cart_empty(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        product = baker.make(Switch)
        baker.make(CartItem, customer=customer, object_id=product.id)

        response = api_client.post("/shop/cart/clear/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(customer=customer).exists()

    def test_if_customer_can_delete_cart_item_return_204_and_deleted(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        cart_item = baker.make(CartItem, customer=customer)

        response = api_client.delete(f"/shop/cart/cart-item/{cart_item.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(id=cart_item.id).exists()
