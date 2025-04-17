import pytest
from model_bakery import baker
from rest_framework import status

from rolt.brand.models import Brand
from rolt.component_types.models import ComponentType
from rolt.components.models.stabilizer_model import Stabilizer


@pytest.mark.django_db
class TestStabilizerApi:
    def test_if_anonymous_user_can_get_stabilizer_list_return_200(self, api_client):
        baker.make(Stabilizer, _quantity=3)
        response = api_client.get("/components/stabilizers/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # noqa: PLR2004

    def test_if_anonymous_user_can_get_stabilizer_detail_return_200(self, api_client):
        stabilizer = baker.make(Stabilizer)
        response = api_client.get(f"/components/stabilizers/{stabilizer.code}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == stabilizer.label

    def test_if_anonymous_user_can_not_create_stabilizer_return_403(self, api_client):
        response = api_client.post("/components/stabilizers/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_update_stabilizer_return_403(self, api_client):
        stabilizer = baker.make(Stabilizer)
        response = api_client.patch(
            f"/components/stabilizers/{stabilizer.code}/update/",
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_can_not_delete_stabilizer_return_403(self, api_client):
        stabilizer = baker.make(Stabilizer)
        response = api_client.delete(
            f"/components/stabilizers/{stabilizer.code}/delete/",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_employee_is_product_manager_can_create_stabilizer_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BR123")
        type = baker.make(ComponentType, code="MT123")  # noqa: A001
        data = {
            "code": "stab001",
            "label": "Test Stabilizer",
            "brand_code": brand.code,
            "mount_code": type.code,
            "is_lubed": True,
            "description": "Test desc",
            "price": 7.50,
        }
        response = api_client.post(
            "/components/stabilizers/create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Stabilizer.objects.filter(code="stab001").exists()

    def test_if_employee_is_product_manager_can_update_stabilizer_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand, code="BRCODE")
        type = baker.make(ComponentType, code="MTCODE")  # noqa: A001
        stabilizer = baker.make(Stabilizer)
        update_data = {
            "label": "Updated Label",
            "brand_code": brand.code,
            "mount_code": type.code,
            "is_lubed": False,
            "description": "Updated desc",
            "price": 8.25,
        }
        response = api_client.patch(
            f"/components/stabilizers/{stabilizer.code}/update/",
            data=update_data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Stabilizer.objects.filter(label="Updated Label").exists()

    def test_if_employee_is_product_manager_can_delete_stabilizer_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        stabilizer = baker.make(Stabilizer)
        response = api_client.delete(
            f"/components/stabilizers/{stabilizer.code}/delete/",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Stabilizer.objects.filter(code=stabilizer.code).exists()

    def test_if_employee_is_product_manager_can_bulk_create_stabilizers_return_201(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        make_employee_is_product_manager()
        brand = baker.make(Brand)
        type = baker.make(ComponentType)  # noqa: A001
        data = [
            {
                "code": "stab_1",
                "label": "Stabilizer 1",
                "brand_code": brand.code,
                "mount_code": type.code,
                "is_lubed": True,
                "description": "Desc 1",
                "price": 5.0,
                "image": None,
            },
            {
                "code": "stab_2",
                "label": "Stabilizer 2",
                "brand_code": brand.code,
                "mount_code": type.code,
                "is_lubed": False,
                "description": "Desc 2",
                "price": 6.0,
                "image": None,
            },
        ]
        response = api_client.post(
            "/components/stabilizers/bulk-create/",
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Stabilizer.objects.filter(code="stab_1").exists()
        assert Stabilizer.objects.filter(code="stab_2").exists()

    def test_if_anonymous_user_can_filter_stabilizer_by_label_return_200(
        self,
        api_client,
    ):
        baker.make(Stabilizer, label="Silent Black")
        baker.make(Stabilizer, label="Transparent Blue")
        response = api_client.get("/components/stabilizers/?label=Black")
        assert response.status_code == status.HTTP_200_OK
        assert any("Black" in stab["label"] for stab in response.data)

    def test_if_anonymous_user_can_filter_stabilizer_by_brand_code_return_200(
        self,
        api_client,
    ):
        brand = baker.make(Brand, code="GAT")
        baker.make(Stabilizer, brand=brand)
        response = api_client.get("/components/stabilizers/?brand_code=GAT")
        assert response.status_code == status.HTTP_200_OK

    def test_if_anonymous_user_can_filter_stabilizer_by_mount_code_return_200(
        self,
        api_client,
    ):
        mount = baker.make(ComponentType, code="MX")
        baker.make(Stabilizer, mount=mount)
        response = api_client.get("/components/stabilizers/?mount_code=MX")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["mount"]["code"] == "MX"

    def test_if_anonymous_user_can_filter_stabilizer_by_is_lubed_return_200(
        self,
        api_client,
    ):
        baker.make(Stabilizer, is_lubed=True)
        baker.make(Stabilizer, is_lubed=False)
        response = api_client.get("/components/stabilizers/?is_lubed=True")
        assert response.status_code == status.HTTP_200_OK
        assert all(stab["is_lubed"] for stab in response.data)

    def test_if_anonymous_user_can_filter_stabilizer_by_price_range_return_200(
        self,
        api_client,
    ):
        baker.make(Stabilizer, price=5.00)
        baker.make(Stabilizer, price=10.00)
        response = api_client.get("/components/stabilizers/?price_min=4&price_max=6")
        assert response.status_code == status.HTTP_200_OK
        assert all(4 <= float(stab["price"]) <= 6 for stab in response.data)  # noqa: PLR2004

    def test_if_anonymous_user_can_filter_stabilizer_by_multiple_criteria_return_200(
        self,
        api_client,
    ):
        brand = baker.make(Brand, code="DUCKY")
        mount = baker.make(ComponentType, code="CHERRY")
        baker.make(
            Stabilizer,
            label="Silent Red",
            brand=brand,
            mount=mount,
            is_lubed=True,
            price=7.50,
        )
        response = api_client.get(
            "/components/stabilizers/?label=Silent&brand_code=DUCKY&mount_code=CHERRY&is_lubed=True&price_min=7&price_max=8",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["label"] == "Silent Red"
        assert response.data[0]["brand"]["code"] == "DUCKY"
        assert response.data[0]["mount"]["code"] == "CHERRY"
        assert response.data[0]["is_lubed"] is True
        assert 7 <= float(response.data[0]["price"]) <= 8  # noqa: PLR2004
