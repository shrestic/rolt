import pytest
from model_bakery import baker
from rest_framework import status

from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestManufacturer:
    def test_if_anonymous_user_can_get_manufacturer_list_return_200(self, api_client):
        # Arrange
        baker.make(Manufacturer, _quantity=3)

        # Act
        response = api_client.get("/manufacturers/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_manufacturer_detail_return_200(self, api_client):
        # Arrange
        manufacturer = baker.make(Manufacturer)

        # Act
        response = api_client.get(f"/manufacturers/{manufacturer.code}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == manufacturer.label

    def test_if_anonymous_user_can_not_create_manufacturer_return_403(self, api_client):
        # Act
        response = api_client.post("/manufacturers/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_manufacturer_return_403(self, api_client):
        # Arrange
        manufacturer = baker.make(Manufacturer)

        # Act
        response = api_client.patch(f"/manufacturers/{manufacturer.code}/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_manufacturer_return_403(self, api_client):
        # Arrange
        manufacturer = baker.make(Manufacturer)

        # Act
        response = api_client.delete(f"/manufacturers/{manufacturer.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_manufacturer_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        manufacturer_data = {
            "code": "test_mfr",
            "label": "Test Manufacturer",
            "logo": None,
        }

        # Act
        response = api_client.post(
            "/manufacturers/create/",
            data=manufacturer_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Manufacturer.objects.filter(label="Test Manufacturer").exists()

    def test_if_employee_is_product_manager_can_update_manufacturer_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer)
        update_data = {"label": "Updated Manufacturer"}

        # Act
        response = api_client.patch(
            f"/manufacturers/{manufacturer.code}/update/",
            data=update_data,
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert Manufacturer.objects.filter(label="Updated Manufacturer").exists()

    def test_if_employee_is_product_manager_can_delete_manufacturer_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer)

        # Act
        response = api_client.delete(f"/manufacturers/{manufacturer.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Manufacturer.objects.filter(code=manufacturer.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_manufacturer_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        data = [
            {
                "code": "durock",
                "label": "Durock",
                "logo": None,
            },
            {
                "code": "akko",
                "label": "Akko",
                "logo": None,
            },
        ]

        # Act
        response = api_client.post(
            "/manufacturers/bulk-create/",
            data=data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 2  # noqa: PLR2004
        assert Manufacturer.objects.filter(code="durock").exists()
        assert Manufacturer.objects.filter(code="akko").exists()
