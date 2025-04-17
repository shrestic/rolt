import pytest
from model_bakery import baker
from rest_framework import status

from rolt.brand.models import Brand
from rolt.component_types.models import ComponentType
from rolt.components.models.case_model import Case


@pytest.mark.django_db
class TestCaseApi:
    def test_if_anonymous_user_can_get_case_list_return_200(self, api_client):
        baker.make(Case, _quantity=3)
        response = api_client.get("/components/cases/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_case_detail_return_200(self, api_client):
        case = baker.make(Case)
        response = api_client.get(f"/components/cases/{case.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == case.label

    def test_if_anonymous_user_can_not_create_case_return_403(self, api_client):
        response = api_client.post("/components/cases/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_case_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="B01")
        material = baker.make(ComponentType, code="MAT01")
        mount_style = baker.make(ComponentType, code="MT01")
        data = {
            "code": "case001",
            "label": "Acrylic 65%",
            "brand_code": brand.code,
            "material_code": material.code,
            "color": "Black",
            "mount_style_code": mount_style.code,
            "price": 79.99,
            "description": "Clear case with gasket mount",
        }
        response = api_client.post(
            "/components/cases/create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Case.objects.filter(code="case001").exists()

    def test_if_employee_is_product_manager_can_update_case_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        case = baker.make(Case)
        new_brand = baker.make(Brand, code="B02")
        new_material = baker.make(ComponentType, code="MAT02")
        new_mount_style = baker.make(ComponentType, code="MT02")
        data = {
            "label": "Updated Case",
            "brand_code": new_brand.code,
            "material_code": new_material.code,
            "mount_style_code": new_mount_style.code,
            "price": 120.0,
        }
        response = api_client.patch(
            f"/components/cases/{case.code}/update/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Case.objects.filter(label="Updated Case").exists()

    def test_if_employee_is_product_manager_can_delete_case_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        case = baker.make(Case)
        response = api_client.delete(f"/components/cases/{case.code}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Case.objects.filter(code=case.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_case_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand)
        material = baker.make(ComponentType)
        mount_style = baker.make(ComponentType)
        data = [
            {
                "code": "case_bulk_1",
                "label": "Bulk Case 1",
                "brand_code": brand.code,
                "material_code": material.code,
                "mount_style_code": mount_style.code,
                "color": "Black",
                "price": 65.0,
                "image": None,
                "description": "",
            },
            {
                "code": "case_bulk_2",
                "label": "Bulk Case 2",
                "brand_code": brand.code,
                "material_code": material.code,
                "mount_style_code": mount_style.code,
                "color": "White",
                "price": 89.0,
                "image": None,
                "description": "",
            },
        ]
        response = api_client.post(
            "/components/cases/bulk-create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Case.objects.filter(code="case_bulk_1").exists()
        assert Case.objects.filter(code="case_bulk_2").exists()

    def test_if_anonymous_user_can_filter_case_by_label(self, api_client):
        baker.make(Case, label="Clear Case")
        response = api_client.get("/components/cases/?label=clear")
        assert response.status_code == status.HTTP_200_OK
        assert "Clear" in response.data[0]["label"]

    def test_if_anonymous_user_can_filter_case_by_price_range(self, api_client):
        baker.make(Case, price=70)
        baker.make(Case, price=110)
        response = api_client.get("/components/cases/?price_min=60&price_max=80")
        assert response.status_code == status.HTTP_200_OK
        assert all(60 <= float(c["price"]) <= 80 for c in response.data)  # noqa: PLR2004

    def test_if_anonymous_user_can_filter_case_by_brand_code(self, api_client):
        brand = baker.make(Brand, code="TKC")
        baker.make(Case, brand=brand)
        response = api_client.get(f"/components/cases/?brand_code={brand.code}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["brand"]["code"] == brand.code
