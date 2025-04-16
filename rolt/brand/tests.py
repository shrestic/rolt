import pytest
from model_bakery import baker
from rest_framework import status

from rolt.brand.models import Brand


@pytest.mark.django_db
class TestBrand:
    def test_if_anonymous_user_can_get_brand_list_return_200(self, api_client):
        # Arrange
        baker.make(Brand, _quantity=3)

        # Act
        response = api_client.get("/brands/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_brand_detail_return_200(self, api_client):
        # Arrange
        brand = baker.make(Brand)

        # Act
        response = api_client.get(f"/brands/{brand.code}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == brand.label

    def test_if_anonymous_user_can_not_create_brand_return_403(self, api_client):
        # Act
        response = api_client.post("/brands/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_brand_return_403(self, api_client):
        # Arrange
        brand = baker.make(Brand)

        # Act
        response = api_client.patch(f"/brands/{brand.code}/update/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_brand_return_403(self, api_client):
        # Arrange
        brand = baker.make(Brand)

        # Act
        response = api_client.delete(f"/brands/{brand.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_brand_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand_data = {
            "code": "test_brand",
            "label": "Test Brand",
            "logo": None,
        }

        # Act
        response = api_client.post(
            "/brands/create/",
            data=brand_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Brand.objects.filter(label="Test Brand").exists()

    def test_if_employee_is_product_manager_can_update_brand_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand)
        update_data = {"label": "Updated Brand"}

        # Act
        response = api_client.patch(
            f"/brands/{brand.code}/update/",
            data=update_data,
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert Brand.objects.filter(label="Updated Brand").exists()

    def test_if_employee_is_product_manager_can_delete_brand_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand)

        # Act
        response = api_client.delete(f"/brands/{brand.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Brand.objects.filter(code=brand.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_brand_return_201(
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
            "/brands/bulk-create/",
            data=data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 2  # noqa: PLR2004
        assert Brand.objects.filter(code="durock").exists()
        assert Brand.objects.filter(code="akko").exists()
