import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.switch_model import Switch
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestSwitchApis:
    def test_if_anonymous_user_can_get_switch_list_return_200(self, api_client):
        baker.make(Switch, _quantity=3)
        response = api_client.get("/components/switches/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_switch_detail_return_200(self, api_client):
        switch = baker.make(Switch)
        response = api_client.get(f"/components/switches/{switch.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == switch.code

    def test_if_anonymous_user_can_not_create_switch_return_403(self, api_client):
        response = api_client.post("/components/switches/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_can_create_switch_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="GATERON")
        switch_data = {
            "code": "GAT_YELLOW",
            "name": "Gateron Yellow",
            "manufacturer_code": manufacturer.code,
            "type": "Linear",
            "actuation_force": 50,
            "bottom_out_force": 67,
            "pre_travel": 2.0,
            "total_travel": 4.0,
            "sound_level": "Medium",
            "factory_lubed": True,
            "stem_material": "POM",
            "housing_material": "Polycarbonate",
            "pin_type": "5-pin",
            "led_support": True,
            "led_position": "South-facing",
            "lifespan": 60000000,
            "compatible_with": "MX",
            "image": None,
            "price_per_switch": 4,
            "description": "A smooth linear switch with a light actuation force.",
        }
        response = api_client.post(
            "/components/switches/create/",
            data=switch_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Switch.objects.filter(code="GAT_YELLOW").exists()

    def test_filter_switches_by_type_return_200(self, api_client):
        baker.make(Switch, type="Linear")
        baker.make(Switch, type="Tactile")
        response = api_client.get("/components/switches/?type=Linear")
        assert response.status_code == status.HTTP_200_OK
        assert all(s["type"] == "Linear" for s in response.data["results"])

    def test_filter_switches_by_price_range_return_200(self, api_client):
        baker.make(Switch, price_per_switch=2)
        baker.make(Switch, price_per_switch=5)
        baker.make(Switch, price_per_switch=8)
        response = api_client.get("/components/switches/?price_min=3&price_max=6")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert float(response.data["results"][0]["price_per_switch"]) == 5  # noqa: PLR2004

    def test_filter_switches_by_factory_lubed_and_led_support(self, api_client):
        baker.make(Switch, factory_lubed=True, led_support=True)
        baker.make(Switch, factory_lubed=False, led_support=False)
        response = api_client.get(
            "/components/switches/?factory_lubed=true&led_support=true",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["factory_lubed"] is True

    def test_filter_switches_by_manufacturer_code(self, api_client):
        manufacturer = baker.make(Manufacturer, code="GAT")
        baker.make(Switch, manufacturer=manufacturer)
        response = api_client.get("/components/switches/?manufacturer_code=GAT")
        assert response.status_code == status.HTTP_200_OK

    def test_if_anonymous_user_gets_empty_list_when_no_switches_exist(
        self,
        api_client,
    ):
        response = api_client.get("/components/switches/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_if_get_switch_detail_returns_404_for_nonexistent_switch(
        self,
        api_client,
    ):
        response = api_client.get("/components/switches/nonexistent-code/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Switch not found"

    def test_if_employee_cannot_create_switch_with_existing_code(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="GATERON")
        baker.make(Switch, code="GAT_YELLOW", manufacturer=manufacturer)
        switch_data = {
            "code": "GAT_YELLOW",
            "name": "Duplicate Switch",
            "manufacturer_code": manufacturer.code,
            "type": "Linear",
            "actuation_force": 50,
            "bottom_out_force": 67,
            "pre_travel": 2.0,
            "total_travel": 4.0,
            "sound_level": "Medium",
            "factory_lubed": True,
            "stem_material": "POM",
            "housing_material": "Polycarbonate",
            "pin_type": "5-pin",
            "led_support": True,
            "led_position": "South-facing",
            "lifespan": 60000000,
            "compatible_with": "MX",
            "image": None,
            "price_per_switch": 4,
        }
        response = api_client.post(
            "/components/switches/create/",
            data=switch_data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["extra"]["fields"]["code"][0]
            == "Switch with this code already exists."
        )

    def test_if_employee_cannot_create_switch_with_invalid_manufacturer_code(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        switch_data = {
            "code": "INVALID_MANUFACTURER",
            "name": "Invalid Manufacturer Switch",
            "manufacturer_code": "INVALID_CODE",
            "type": "Linear",
            "actuation_force": 50,
            "bottom_out_force": 67,
            "pre_travel": 2.0,
            "total_travel": 4.0,
            "sound_level": "Medium",
            "factory_lubed": True,
            "stem_material": "POM",
            "housing_material": "Polycarbonate",
            "pin_type": "5-pin",
            "led_support": True,
            "led_position": "South-facing",
            "lifespan": 60000000,
            "compatible_with": "MX",
            "image": None,
            "price_per_switch": 4,
        }
        response = api_client.post(
            "/components/switches/create/",
            data=switch_data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Manufacturer not found" in response.data["message"]

    def test_if_filter_switches_by_nonexistent_type_returns_empty_list(
        self,
        api_client,
    ):
        baker.make(Switch, type="Linear")
        response = api_client.get("/components/switches/?type=NonexistentType")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_if_filter_switches_by_invalid_price_range_returns_empty_list(
        self,
        api_client,
    ):
        baker.make(Switch, price_per_switch=10)
        response = api_client.get("/components/switches/?price_min=20&price_max=30")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_if_filter_switches_with_invalid_boolean_field_returns_400(
        self,
        api_client,
    ):
        response = api_client.get("/components/switches/?factory_lubed=invalid")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_employee_can_bulk_create_switches_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="GATERON")
        switches_data = [
            {
                "code": "GAT_RED",
                "name": "Gateron Red",
                "manufacturer_code": manufacturer.code,
                "type": "Linear",
                "actuation_force": 45,
                "bottom_out_force": 60,
                "pre_travel": 2.0,
                "total_travel": 4.0,
                "sound_level": "Low",
                "factory_lubed": False,
                "stem_material": "POM",
                "housing_material": "Polycarbonate",
                "pin_type": "5-pin",
                "led_support": True,
                "led_position": "South-facing",
                "lifespan": 60000000,
                "compatible_with": "MX",
                "image": None,
                "price_per_switch": 3,
            },
            {
                "code": "GAT_BLUE",
                "name": "Gateron Blue",
                "manufacturer_code": manufacturer.code,
                "type": "Clicky",
                "actuation_force": 55,
                "bottom_out_force": 65,
                "pre_travel": 2.2,
                "total_travel": 4.0,
                "sound_level": "High",
                "factory_lubed": False,
                "stem_material": "POM",
                "housing_material": "Polycarbonate",
                "pin_type": "5-pin",
                "led_support": True,
                "led_position": "South-facing",
                "lifespan": 60000000,
                "compatible_with": "MX",
                "image": None,
                "price_per_switch": 4,
            },
        ]
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=switches_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Switch.objects.filter(code="GAT_RED").exists()
        assert Switch.objects.filter(code="GAT_BLUE").exists()

    def test_if_bulk_create_fails_with_duplicate_codes(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="GATERON")
        baker.make(Switch, code="GAT_RED", manufacturer=manufacturer)
        switches_data = [
            {
                "code": "GAT_RED",
                "name": "Duplicate Red",
                "manufacturer_code": manufacturer.code,
                "type": "Linear",
                "actuation_force": 45,
                "bottom_out_force": 60,
                "pre_travel": 2.0,
                "total_travel": 4.0,
                "sound_level": "Low",
                "factory_lubed": False,
                "stem_material": "POM",
                "housing_material": "Polycarbonate",
                "pin_type": "5-pin",
                "led_support": True,
                "led_position": "South-facing",
                "lifespan": 60000000,
                "compatible_with": "MX",
                "image": None,
                "price_per_switch": 3,
            },
        ]
        response = api_client.post(
            "/components/switches/bulk-create/",
            data=switches_data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exist" in response.data["extra"]["fields"][0]["code"][0]
