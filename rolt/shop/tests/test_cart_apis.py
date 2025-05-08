import pytest
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from rest_framework import status

from rolt.components.models.switch_model import Switch
from rolt.inventory.models import SwitchInventory
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

        # Create a switch with inventory
        switch = baker.make(Switch, price_per_switch=0.5)

        # Set inventory quantity - enough for the cart item
        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 20  # Set more than requested quantity
        switch_inv.save()

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

        # Verify the cart item was created with correct details
        cart_item = CartItem.objects.get(customer=customer)
        assert cart_item.quantity == 10  # noqa: PLR2004
        assert str(cart_item.object_id) == str(switch.id)

    def test_if_customer_can_view_cart_items_return_200_and_list(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        # Create a switch with inventory
        switch = baker.make(Switch)

        # Set inventory quantity
        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 15
        switch_inv.save()

        # Import needed models for content_type
        from django.contrib.contenttypes.models import ContentType

        # Get content type for Switch model
        switch_content_type = ContentType.objects.get_for_model(Switch)

        # Create cart item with proper content_type
        baker.make(
            CartItem,
            customer=customer,
            content_type=switch_content_type,
            object_id=switch.id,
            quantity=5,
        )

        response = api_client.get("/shop/cart/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 1

    def test_if_customer_can_clear_cart_return_204_and_cart_empty(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        # Create a switch with inventory
        switch = baker.make(Switch)

        # Set inventory quantity
        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 10
        switch_inv.save()

        # Import needed models for content_type
        from django.contrib.contenttypes.models import ContentType

        # Get content type for Switch model
        switch_content_type = ContentType.objects.get_for_model(Switch)

        # Create cart item with proper content_type
        baker.make(
            CartItem,
            customer=customer,
            content_type=switch_content_type,
            object_id=switch.id,
            quantity=3,
        )

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

        # Create a switch with inventory
        switch = baker.make(Switch)

        # Set inventory quantity
        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 8
        switch_inv.save()

        # Get content type for Switch model
        switch_content_type = ContentType.objects.get_for_model(Switch)

        # Create cart item with proper content_type
        cart_item = baker.make(
            CartItem,
            customer=customer,
            content_type=switch_content_type,
            object_id=switch.id,
            quantity=2,
        )

        response = api_client.delete(f"/shop/cart/cart-item/{cart_item.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(id=cart_item.id).exists()

    def test_if_inventory_is_checked_when_adding_to_cart_return_400_for_insufficient_stock(  # noqa: E501
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        user = customer.user
        api_client.force_authenticate(user=user)

        # Create a switch with limited inventory
        switch = baker.make(Switch, price_per_switch=0.5)

        # Set inventory quantity to less than what will be requested
        switch_inv = SwitchInventory.objects.get(switch=switch)
        switch_inv.quantity = 5  # Only 5 in stock
        switch_inv.save()

        # Verify initial inventory level
        assert SwitchInventory.objects.get(switch=switch).quantity == 5  # noqa: PLR2004

        # Try to add more than available in inventory
        payload = {
            "product_type": "switch",
            "product_id": str(switch.id),
            "quantity": 10,  # Requesting more than available
        }

        # This should fail with a 400 because there's not enough stock
        response = api_client.post(
            "/shop/cart/cart-item/create/",
            data=payload,
            format="json",
        )

        # Verify the response status code
        assert response.status_code == status.HTTP_400_BAD_REQUEST
