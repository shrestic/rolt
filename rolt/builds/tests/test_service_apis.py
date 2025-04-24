import pytest
from rest_framework import status

from rolt.builds.models import Service


@pytest.mark.django_db
class TestServiceApi:
    def test_if_product_manager_can_create_service_return_201_and_service_created(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        payload = {
            "code": "LUBE_SERVICE",
            "name": "Lube Switches",
            "price": "15.00",
            "description": "Lube all your switches for smoother feel",
        }

        response = api_client.post(
            "/builds/services/create/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Service.objects.filter(code="LUBE_SERVICE").exists()

    def test_if_product_manager_create_duplicate_service_code_return_400(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        Service.objects.create(code="DUPLICATE", name="Dup", price=5)

        payload = {
            "code": "DUPLICATE",
            "name": "New Dup",
            "price": "10.00",
        }

        response = api_client.post(
            "/builds/services/create/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_product_manager_can_delete_service_return_204_and_deleted(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        Service.objects.create(code="DELETE_ME", name="Temp", price=1)

        response = api_client.delete("/builds/services/DELETE_ME/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Service.objects.filter(code="DELETE_ME").exists()

    def test_if_product_manager_can_update_service_return_200_and_updated(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        service = Service.objects.create(code="UPDATE_ME", name="Temp", price=1)

        payload = {
            "name": "Updated Name",
            "price": "20.00",
        }

        response = api_client.patch(
            f"/builds/services/{service.code}/update/",
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        service.refresh_from_db()
        assert service.name == "Updated Name"
        assert service.price == 20.00  # noqa: PLR2004

    def test_if_delete_nonexistent_service_return_400(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        user = make_employee_is_product_manager()
        api_client.force_authenticate(user=user)

        response = api_client.delete("/builds/services/NOT_FOUND/delete/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
