import pytest
from model_bakery import baker
from rest_framework import status

from rolt.brand.models import Brand
from rolt.component_types.models import ComponentType
from rolt.components.models.switch_model import Switch


@pytest.mark.django_db
class TestSwitchApi:
    def test_if_anonymous_user_can_get_switch_list_return_200(self, api_client):
        # Arrange
        baker.make(Switch, _quantity=3)

        # Act
        response = api_client.get("/components/switches/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_switch_detail_return_200(self, api_client):
        # Arrange
        switch = baker.make(Switch)

        # Act
        response = api_client.get(f"/components/switches/{switch.code}/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == switch.label
        assert response.data["brand"]["code"] == switch.brand.code
        assert response.data["type"]["code"] == switch.type.code
        assert response.data["is_lubed"] == switch.is_lubed

    def test_if_anonymous_user_can_not_create_switch_return_403(self, api_client):
        # Act
        response = api_client.post("/components/switches/create/", {})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_switch_return_403(self, api_client):
        # Arrange
        switch = baker.make(Switch)

        # Act
        response = api_client.patch(
            f"/components/switches/{switch.code}/update/",
            {},
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_switch_return_403(self, api_client):
        # Arrange
        switch = baker.make(Switch)

        # Act
        response = api_client.delete(f"/components/switches/{switch.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_switch_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BSDC2")
        type = baker.make(ComponentType, code="HSNC76")  # noqa: A001
        switch_data = {
            "code": "test_switch",
            "label": "Test Switch",
            "brand_code": brand.code,
            "type_code": type.code,
            "is_lubed": True,
            "description": "Test description",
            "price": 10.99,
        }

        # Act
        response = api_client.post(
            "/components/switches/create/",
            data=switch_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Switch.objects.filter(label="Test Switch").exists()

    def test_if_employee_is_product_manager_can_update_switch_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BSDC2")
        type = baker.make(ComponentType, code="HSNC76")  # noqa: A001
        switch = baker.make(Switch)
        update_data = {
            "label": "Updated Switch",
            "brand_code": brand.code,
            "type_code": type.code,
            "is_lubed": False,
            "description": "Updated description",
            "price": 12.99,
        }

        # Act
        response = api_client.patch(
            f"/components/switches/{switch.code}/update/",
            data=update_data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert Switch.objects.filter(label="Updated Switch").exists()

    def test_if_employee_is_product_manager_can_delete_switch_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        switch = baker.make(Switch)

        # Act
        response = api_client.delete(f"/components/switches/{switch.code}/delete/")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Switch.objects.filter(code=switch.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_switches_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brands = baker.make(Brand, _quantity=2)
        types = baker.make(ComponentType, _quantity=2)
        switches_data = [
            {
                "code": "switch_1",
                "label": "Switch 1",
                "brand_code": brands[0].code,
                "type_code": types[0].code,
                "is_lubed": True,
                "description": "Description 1",
                "price": 9.99,
                "image": None,
            },
            {
                "code": "switch_2",
                "label": "Switch 2",
                "brand_code": brands[1].code,
                "type_code": types[1].code,
                "is_lubed": False,
                "description": "Description 2",
                "price": 14.99,
                "image": None,
            },
        ]

        # Act
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=switches_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Switch.objects.filter(code="switch_1").exists()
        assert Switch.objects.filter(code="switch_2").exists()

    def test_if_employee_is_product_manager_bulk_create_with_invalid_brand_code_return_400(  # noqa: E501
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        invalid_switches_data = [
            {
                "code": "switch_1",
                "label": "Switch 1",
                "brand_code": "INVALID_BRAND",
                "type_code": "INVALID_TYPE",
                "is_lubed": True,
                "description": "Description 1",
                "price": 9.99,
                "image": None,
            },
            {
                "code": "switch_2",
                "label": "Switch 2",
                "brand_code": "INVALID_BRAND",
                "type_code": "INVALID_TYPE",
                "is_lubed": False,
                "description": "Description 2",
                "price": 14.99,
                "image": None,
            },
        ]

        # Act
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=invalid_switches_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "Brand with code 'INVALID_BRAND' does not exist."
        )

    def test_if_employee_is_product_manager_bulk_create_with_invalid_type_code_return_400(  # noqa: E501
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="VALID_BRAND")
        invalid_switches_data = [
            {
                "code": "switch_1",
                "label": "Switch 1",
                "brand_code": brand.code,
                "type_code": "INVALID_TYPE",
                "is_lubed": True,
                "description": "Description 1",
                "price": 9.99,
                "image": None,
            },
            {
                "code": "switch_2",
                "label": "Switch 2",
                "brand_code": brand.code,
                "type_code": "INVALID_TYPE",
                "is_lubed": False,
                "description": "Description 2",
                "price": 14.99,
                "image": None,
            },
        ]

        # Act
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=invalid_switches_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "ComponentType with code 'INVALID_TYPE' does not exist."
        )

    def test_if_employee_is_product_manager_bulk_create_with_duplicate_code_return_400(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BR1")
        type = baker.make(ComponentType, code="TYPE1")  # noqa: A001
        baker.make(Switch, code="switch_1")

        duplicate_data = [
            {
                "code": "switch_1",
                "label": "Duplicated Switch",
                "brand_code": brand.code,
                "type_code": type.code,
                "is_lubed": True,
                "description": "Duplicated",
                "price": 10.0,
                "image": None,
            },
        ]

        # Act
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=duplicate_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Switch with code 'switch_1' already exists."

    def test_if_employee_is_product_manager_bulk_create_with_existing_brand_type_combo_return_400(  # noqa: E501
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        # Arrange
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BR1")
        type = baker.make(ComponentType, code="TYPE1")  # noqa: A001

        baker.make(Switch, brand=brand, type=type)

        duplicated_combo_data = [
            {
                "code": "new_switch",
                "label": "New Switch",
                "brand_code": brand.code,
                "type_code": type.code,
                "is_lubed": True,
                "description": "Duplicated combo",
                "price": 15.0,
                "image": None,
            },
        ]

        # Act
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=duplicated_combo_data,
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == (
            f"Switch with brand '{brand.code}' and type '{type.code}' already exists."
        )

    def test_if_anonymous_user_can_filter_switches_by_label_return_200(
        self,
        api_client,
    ):
        # Arrange
        baker.make(Switch, label="Test Label 1")
        baker.make(Switch, label="Test Label 2")

        # Act
        response = api_client.get("/components/switches/?label=Test Label 1")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["label"] == "Test Label 1"

    def test_if_anonymous_user_can_filter_switches_by_brand_code_return_200(
        self,
        api_client,
    ):
        # Arrange
        brand = baker.make(Brand, code="BRAND1")
        baker.make(Switch, brand=brand)

        # Act
        response = api_client.get("/components/switches/?brand_code=BRAND1")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["brand"]["code"] == brand.code

    def test_if_anonymous_user_can_filter_switches_by_type_code_return_200(
        self,
        api_client,
    ):
        # Arrange
        type = baker.make(ComponentType, code="TYPE1")  # noqa: A001
        baker.make(Switch, type=type)

        # Act
        response = api_client.get("/components/switches/?type_code=TYPE1")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["type"]["code"] == type.code

    def test_if_anonymous_user_can_filter_switches_by_price_range_return_200(
        self,
        api_client,
    ):
        # Arrange
        baker.make(Switch, price=5.00)
        baker.make(Switch, price=15.00)
        baker.make(Switch, price=25.00)

        # Act
        response = api_client.get("/components/switches/?price_min=10&price_max=20")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["price"] == "15.00"

    def test_if_anonymous_user_can_filter_switches_by_is_lubed_return_200(
        self,
        api_client,
    ):
        # Arrange
        baker.make(Switch, is_lubed=True)
        baker.make(Switch, is_lubed=False)

        # Act
        response = api_client.get("/components/switches/?is_lubed=True")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["is_lubed"] is True

    def test_if_anonymous_user_can_filter_switches_by_multiple_criteria_return_200(
        self,
        api_client,
    ):
        # Arrange
        brand = baker.make(Brand, code="BRAND1")
        type = baker.make(ComponentType, code="TYPE1")  # noqa: A001
        baker.make(
            Switch,
            label="Test Label",
            brand=brand,
            type=type,
            price=15.00,
            is_lubed=True,
        )
        baker.make(Switch, label="Other Label", price=25.00, is_lubed=False)

        # Act
        response = api_client.get(
            "/components/switches/?label=Test Label"
            "&brand_code=BRAND1"
            "&type_code=TYPE1"
            "&price_min=10"
            "&price_max=20"
            "&is_lubed=True",
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["label"] == "Test Label"
        assert response.data[0]["brand"]["code"] == brand.code
        assert response.data[0]["type"]["code"] == type.code
        assert response.data[0]["price"] == "15.00"
        assert response.data[0]["is_lubed"] is True

    def test_if_anonymous_user_can_filter_switches_by_type_return_200(
        self,
        api_client,
    ):
        # Arrange
        type = baker.make(ComponentType, label="Linear")  # noqa: A001
        baker.make(Switch, type=type)

        # Act
        response = api_client.get("/components/switches/?type=Linear")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["type"]["label"] == type.label

    def test_if_anonymous_user_can_filter_switches_by_brand_return_200(
        self,
        api_client,
    ):
        # Arrange
        brand = baker.make(Brand, label="BrandX")
        baker.make(Switch, brand=brand)

        # Act
        response = api_client.get("/components/switches/?brand=BrandX")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["brand"]["label"] == brand.label
