import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.switch_model import Switch
from rolt.shop.models.cart_model import Cart


@pytest.mark.django_db
class TestCartApi:
    def test_customer_can_create_cart_item(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        switch = baker.make(Switch)

        payload = {
            "product_type": "switch",
            "product_id": str(switch.id),
            "quantity": 10,
        }

        response = api_client.post("/shop/cart/create/", data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Cart.objects.filter(customer=customer).exists()

    def test_customer_can_view_cart_items(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        product = baker.make(Switch)
        baker.make(Cart, customer=customer, object_id=product.id)

        response = api_client.get("/shop/cart/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_customer_can_clear_cart(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        product = baker.make(Switch)
        baker.make(Cart, customer=customer, object_id=product.id)

        response = api_client.post("/shop/cart/clear/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cart.objects.filter(customer=customer).exists()

    def test_customer_can_delete_cart_item(self, api_client, make_customer):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        cart_item = baker.make(Cart, customer=customer)

        response = api_client.delete(f"/shop/cart/{cart_item.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cart.objects.filter(id=cart_item.id).exists()
