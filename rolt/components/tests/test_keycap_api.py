import pytest
from model_bakery import baker
from rest_framework import status

from rolt.brand.models import Brand
from rolt.component_types.models import ComponentType
from rolt.components.models.keycap_model import Keycap


@pytest.mark.django_db
class TestKeycapApi:
    def test_if_anonymous_user_can_get_keycap_list_return_200(self, api_client):
        baker.make(Keycap, _quantity=3)
        response = api_client.get("/components/keycaps/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_keycap_detail_return_200(self, api_client):
        keycap = baker.make(Keycap)
        response = api_client.get(f"/components/keycaps/{keycap.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == keycap.label

    def test_if_anonymous_user_can_not_create_keycap_return_403(self, api_client):
        response = api_client.post("/components/keycaps/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_keycap_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="B01")
        material = baker.make(ComponentType, code="MT01")
        profile = baker.make(ComponentType, code="PR01")
        data = {
            "code": "kc001",
            "label": "Test Cap",
            "brand_code": brand.code,
            "material_code": material.code,
            "profile_code": profile.code,
            "theme": "Ocean",
            "price": 9.99,
            "description": "A test keycap",
        }
        res = api_client.post("/components/keycaps/create/", data=data, format="json")
        assert res.status_code == status.HTTP_201_CREATED
        assert Keycap.objects.filter(code="kc001").exists()

    def test_if_employee_is_product_manager_can_update_keycap_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        keycap = baker.make(Keycap)
        new_brand = baker.make(Brand, code="B02")
        new_material = baker.make(ComponentType, code="MT02")
        new_profile = baker.make(ComponentType, code="PR02")
        data = {
            "label": "Updated",
            "brand_code": new_brand.code,
            "material_code": new_material.code,
            "profile_code": new_profile.code,
            "theme": "Sky",
            "price": 14.5,
        }
        res = api_client.patch(
            f"/components/keycaps/{keycap.code}/update/",
            data=data,
            format="json",
        )
        assert res.status_code == status.HTTP_200_OK
        assert Keycap.objects.filter(label="Updated").exists()

    def test_if_employee_is_product_manager_can_delete_keycap_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        keycap = baker.make(Keycap)
        res = api_client.delete(f"/components/keycaps/{keycap.code}/delete/")
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not Keycap.objects.filter(code=keycap.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_keycap_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand)
        material = baker.make(ComponentType)
        profile = baker.make(ComponentType)
        data = [
            {
                "code": "kc_bulk_1",
                "label": "Bulk 1",
                "brand_code": brand.code,
                "material_code": material.code,
                "profile_code": profile.code,
                "theme": "Storm",
                "price": 11.0,
                "image": None,
                "description": "",
            },
            {
                "code": "kc_bulk_2",
                "label": "Bulk 2",
                "brand_code": brand.code,
                "material_code": material.code,
                "profile_code": profile.code,
                "theme": "Fire",
                "price": 12.5,
                "image": None,
                "description": "",
            },
        ]
        res = api_client.post(
            "/components/keycaps/bulk-create/",
            data=data,
            format="json",
        )
        assert res.status_code == status.HTTP_201_CREATED
        assert Keycap.objects.filter(code="kc_bulk_1").exists()
        assert Keycap.objects.filter(code="kc_bulk_2").exists()

    def test_if_anonymous_user_can_filter_keycap_by_theme(self, api_client):
        baker.make(Keycap, theme="Stormy Night")
        res = api_client.get("/components/keycaps/?theme=Storm")
        assert res.status_code == status.HTTP_200_OK
        assert "Storm" in res.data[0]["theme"]

    def test_if_anonymous_user_can_filter_keycap_by_price_range(self, api_client):
        baker.make(Keycap, price=8)
        baker.make(Keycap, price=15)
        res = api_client.get("/components/keycaps/?price_min=7&price_max=10")
        assert res.status_code == status.HTTP_200_OK
        assert all(7 <= float(k["price"]) <= 10 for k in res.data)  # noqa: PLR2004

    def test_if_anonymous_user_can_filter_keycap_by_brand_code(self, api_client):
        brand = baker.make(Brand, code="GMK")
        baker.make(Keycap, brand=brand)
        res = api_client.get(f"/components/keycaps/?brand_code={brand.code}")
        assert res.status_code == status.HTTP_200_OK
        assert res.data[0]["brand"]["code"] == "GMK"
