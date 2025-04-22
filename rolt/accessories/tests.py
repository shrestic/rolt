import pytest
from model_bakery import baker
from rest_framework import status

from rolt.accessories.models import Accessory


@pytest.mark.django_db
class TestAccessoryApi:
    def test_if_anonymous_user_can_list_accessories(self, api_client):
        baker.make(Accessory, _quantity=3)

        response = api_client.get("/accessories/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_retrieve_detail(self, api_client):
        accessory = baker.make(Accessory)

        response = api_client.get(f"/accessories/{accessory.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(accessory.id)

    def test_if_product_manager_can_create_accessory(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        payload = {
            "name": "Test Cable",
            "type": "cable",
            "description": "A coiled cable.",
            "price": "19.99",
            "image": None,
        }

        response = api_client.post("/accessories/create/", data=payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Accessory.objects.filter(id=response.data["id"]).exists()

    def test_if_product_manager_can_update_accessory(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        accessory = baker.make(Accessory, name="Old Name")
        response = api_client.patch(
            f"/accessories/{accessory.id}/update/",
            data={"name": "New Name"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        accessory.refresh_from_db()
        assert accessory.name == "New Name"

    def test_if_product_manager_can_delete_accessory(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        accessory = baker.make(Accessory)
        response = api_client.delete(f"/accessories/{accessory.id}/delete/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Accessory.objects.filter(id=accessory.id).exists()
