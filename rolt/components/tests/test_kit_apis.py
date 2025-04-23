import pytest
from model_bakery import baker
from rest_framework import status

from rolt.components.models.kit_model import Kit
from rolt.manufacturers.models import Manufacturer


@pytest.mark.django_db
class TestKitApis:
    def test_if_anonymous_user_can_get_kit_list_return_200(self, api_client):
        baker.make(Kit, _quantity=3)
        response = api_client.get("/components/kits/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_kit_detail_return_200(self, api_client):
        kit = baker.make(Kit)
        response = api_client.get(f"/components/kits/{kit.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == kit.code

    def test_if_anonymous_user_can_not_create_kit_return_403(self, api_client):
        response = api_client.post("/components/kits/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_can_create_kit_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="MANA")
        kit_data = {
            "code": "KIT001",
            "name": "Mana TKL",
            "manufacturer_code": manufacturer.code,
            "layout": "TKL",
            "number_of_keys": 87,
            "layout_detail": "ANSI",
            "case_spec": "Aluminum",
            "mounting_style": "Top",
            "plate_material": "Brass",
            "stab_mount": "PCB",
            "hot_swap": True,
            "knob": True,
            "rgb_type": "Underglow",
            "firmware_type": "QMK",
            "connectivity": "Wired",
            "dimensions": "360x120x30mm",
            "weight": 1.2,
            "image": None,
            "price": 250,
            "description": "",
        }
        response = api_client.post(
            "/components/kits/create/",
            data=kit_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Kit.objects.filter(code="KIT001").exists()

    def test_if_employee_can_bulk_create_kits_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="MK")
        data = [
            {
                "code": "KIT_B1",
                "name": "B1",
                "manufacturer_code": manufacturer.code,
                "layout": "65%",
                "number_of_keys": 68,
                "layout_detail": "ISO",
                "case_spec": "Plastic",
                "mounting_style": "Gasket",
                "plate_material": "Aluminum",
                "stab_mount": "Plate",
                "hot_swap": True,
                "knob": False,
                "rgb_type": "None",
                "firmware_type": "QMK",
                "connectivity": "Wireless",
                "dimensions": "300x100x30mm",
                "weight": 0.9,
                "image": None,
                "price": 150,
            },
            {
                "code": "KIT_B2",
                "name": "B2",
                "manufacturer_code": manufacturer.code,
                "layout": "60%",
                "number_of_keys": 61,
                "layout_detail": "ANSI",
                "case_spec": "Polycarbonate",
                "mounting_style": "Tray",
                "plate_material": "FR4",
                "stab_mount": "PCB",
                "hot_swap": False,
                "knob": False,
                "rgb_type": "Per-key",
                "firmware_type": "VIA",
                "connectivity": "Bluetooth",
                "dimensions": "290x100x30mm",
                "weight": 0.8,
                "image": None,
                "price": 120,
            },
        ]
        response = api_client.post(
            "/components/kits/bulk-create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Kit.objects.filter(code="KIT_B1").exists()
        assert Kit.objects.filter(code="KIT_B2").exists()

    def test_if_duplicate_code_in_bulk_create_return_400(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        manufacturer = baker.make(Manufacturer, code="MK")
        baker.make(Kit, code="KIT_DUPLICATE")
        data = [
            {
                "code": "KIT_DUPLICATE",
                "name": "Already Exist",
                "manufacturer_code": manufacturer.id,
                "layout": "75%",
                "number_of_keys": 84,
                "layout_detail": "ANSI",
                "case_spec": "Aluminum",
                "mounting_style": "Top",
                "plate_material": "Brass",
                "stab_mount": "PCB",
                "hot_swap": True,
                "knob": False,
                "rgb_type": "Per-key",
                "firmware_type": "QMK",
                "connectivity": "Wired",
                "dimensions": "350x120x30mm",
                "weight": 1.1,
                "image": None,
                "price": 220,
            },
        ]
        response = api_client.post(
            "/components/kits/bulk-create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["extra"]["fields"][0]["code"][0]
            == "Kit with this code already exists."
        )

    def test_filter_kits_by_name_return_200(self, api_client):
        baker.make(Kit, name="Alpha")
        baker.make(Kit, name="Beta")
        response = api_client.get("/components/kits/?name=Alpha")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Alpha"

    def test_filter_kits_by_price_range_return_200(self, api_client):
        baker.make(Kit, price=100)
        baker.make(Kit, price=200)
        baker.make(Kit, price=300)
        response = api_client.get("/components/kits/?price_min=150&price_max=250")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["price"] == "200.00"

    def test_filter_kits_by_layout_and_connectivity_return_200(self, api_client):
        baker.make(Kit, layout="TKL", connectivity="Wired")
        baker.make(Kit, layout="60%", connectivity="Wireless")
        response = api_client.get("/components/kits/?layout=TKL&connectivity=Wired")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["layout"] == "TKL"
        assert response.data["results"][0]["connectivity"] == "Wired"

    def test_filter_kits_by_manufacturer_code_return_200(self, api_client):
        manufacturer = baker.make(Manufacturer, code="MANA")
        baker.make(Kit, manufacturer=manufacturer)
        response = api_client.get("/components/kits/?manufacturer_code=MANA")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["manufacturer"]["code"] == "MANA"

    def test_filter_kits_by_hot_swap_and_knob_return_200(self, api_client):
        baker.make(Kit, hot_swap=True, knob=True)
        baker.make(Kit, hot_swap=False, knob=False)
        response = api_client.get("/components/kits/?hot_swap=True&knob=True")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["hot_swap"] is True
        assert response.data["results"][0]["knob"] is True
