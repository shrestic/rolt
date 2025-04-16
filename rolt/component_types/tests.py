import pytest
from model_bakery import baker
from rest_framework import status

from rolt.component_types.models import ComponentType


@pytest.mark.django_db
class TestComponentType:
    def test_if_anonymous_user_can_get_component_type_list_return_200(self, api_client):
        # Arrange
        baker.make(ComponentType, _quantity=3)

        # Act
        response = api_client.get("/component-types/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_component_type_detail_return_200(
        self,
        api_client,
    ):
        # Arrange
        component_type = baker.make(ComponentType)

        # Act
        response = api_client.get(f"/component-types/{component_type.code}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == component_type.label

    def test_if_anonymous_user_can_not_create_component_type_return_403(
        self,
        api_client,
    ):
        # Act
        response = api_client.post("/component-types/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_component_type_return_403(
        self,
        api_client,
    ):
        # Arrange
        component_type = baker.make(ComponentType)

        # Act
        response = api_client.patch(
            f"/component-types/{component_type.code}/update/",
            {},
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_component_type_return_403(
        self,
        api_client,
    ):
        # Arrange
        component_type = baker.make(ComponentType)

        # Act
        response = api_client.delete(f"/component-types/{component_type.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_component_type_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        component_type_data = {
            "code": "test_component_type",
            "label": "Test Component Type",
            "applies_to": "switch",
            "note": "Test description",
        }

        # Act
        response = api_client.post(
            "/component-types/create/",
            data=component_type_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert ComponentType.objects.filter(label="Test Component Type").exists()

    def test_if_employee_is_product_manager_can_update_component_type_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        component_type = baker.make(ComponentType)
        update_data = {
            "label": "Updated Component Type",
            "applies_to": "switch",
            "note": "Updated description",
        }

        # Act
        response = api_client.patch(
            f"/component-types/{component_type.code}/update/",
            data=update_data,
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert ComponentType.objects.filter(label="Updated Component Type").exists()

    def test_if_employee_is_product_manager_can_delete_component_type_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        component_type = baker.make(ComponentType)

        # Act
        response = api_client.delete(f"/component-types/{component_type.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ComponentType.objects.filter(code=component_type.code).exists()

    def test_if_anonymous_user_can_filter_component_types(self, api_client):
        # Arrange
        ComponentType.objects.create(code="type1", label="Type 1", applies_to="switch")
        ComponentType.objects.create(code="type2", label="Type 2", applies_to="router")
        ComponentType.objects.create(code="type3", label="Type 3", applies_to="switch")

        # Act
        response = api_client.get("/component-types/", {"applies_to": "switch"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # noqa: PLR2004
        assert all(item["applies_to"] == "switch" for item in response.data)

    def test_if_anonymous_user_gets_empty_list_for_non_matching_filter(
        self,
        api_client,
    ):
        # Arrange
        ComponentType.objects.create(code="type1", label="Type 1", applies_to="switch")
        ComponentType.objects.create(code="type2", label="Type 2", applies_to="router")

        # Act
        response = api_client.get("/component-types/", {"applies_to": "firewall"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_if_anonymous_user_can_filter_component_types_by_two_fields(
        self,
        api_client,
    ):
        # Arrange
        ComponentType.objects.create(code="type1", label="Type 1", applies_to="switch")
        ComponentType.objects.create(code="type2", label="Type 2", applies_to="router")
        ComponentType.objects.create(code="type3", label="Type 3", applies_to="switch")
        ComponentType.objects.create(code="type4", label="Type 4", applies_to="switch")

        # Act
        response = api_client.get(
            "/component-types/",
            {"applies_to": "switch", "label": "Type 3"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["label"] == "Type 3"
        assert response.data[0]["applies_to"] == "switch"
