import logging

import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from rest_framework import status

from rolt.components.models.kit_model import Kit
from rolt.shop.apis.order_apis import OrderStatus
from rolt.shop.models import Order
from rolt.shop.models import OrderItem
from rolt.warranty.models import Warranty
from rolt.warranty.models import WarrantyRequest

User = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestWarrantyApis:
    def test_if_customer_can_get_warranty_list_return_200(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        baker.make(Warranty, customer=customer, orderitem=orderitem, _quantity=1)
        response = api_client.get("/warranty/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        logger.info("Test completed successfully")

    def test_if_customer_cannot_get_other_customer_warranty_list_return_empty(
        self,
        api_client,
        make_customer,
    ):
        customer1 = make_customer()
        customer2 = make_customer()
        api_client.force_authenticate(user=customer1.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer2, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        baker.make(Warranty, customer=customer2, orderitem=orderitem, _quantity=1)
        response = api_client.get("/warranty/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_if_customer_can_get_warranty_detail_return_200(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)
        response = api_client.get(f"/warranty/{warranty.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(warranty.id)

    def test_if_customer_cannot_get_other_warranty_detail_return_400(
        self,
        api_client,
        make_customer,
    ):
        customer1 = make_customer()
        customer2 = make_customer()
        api_client.force_authenticate(user=customer1.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer2, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer2, orderitem=orderitem)
        response = api_client.get(f"/warranty/{warranty.id}/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_product_manager_can_void_warranty_return_200(
        self,
        api_client,
        make_customer,
        make_employee_is_product_manager,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)

        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)

        response = api_client.post(
            f"/warranty/{warranty.id}/void/",
            {"note": "Voided due to policy"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_product_manager_cannot_void_nonexistent_warranty_return_400(
        self,
        api_client,
        make_employee_is_product_manager,
    ):
        product_manager = make_employee_is_product_manager()
        api_client.force_authenticate(user=product_manager)
        response = api_client.post(
            "/warranty/123e4567-e89b-12d3-a456-426614174000/void/",
            {"note": "Test"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_product_manager_can_mark_warranty_expired_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
        make_customer,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)

        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        warranty = baker.make(Warranty, orderitem=orderitem, customer=customer)

        response = api_client.post(f"/warranty/{warranty.id}/expire/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_product_manager_can_delete_warranty_return_204(
        self,
        api_client,
        make_employee_is_product_manager,
        make_customer,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)

        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        warranty = baker.make(
            Warranty,
            orderitem=orderitem,
            customer=customer,
        )  # ✅ FIXED

        response = api_client.delete(f"/warranty/{warranty.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Warranty.objects.filter(id=warranty.id).exists()

    def test_if_customer_can_get_warranty_request_list_return_200(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)
        baker.make(WarrantyRequest, customer=customer, warranty=warranty, _quantity=3)
        response = api_client.get("/warranty/request/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3  # noqa: PLR2004

    def test_if_product_manager_can_get_all_warranty_request_list_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
        make_customer,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)

        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        warranty = baker.make(
            Warranty,
            orderitem=orderitem,
            customer=customer,
        )

        baker.make(
            WarrantyRequest,
            warranty=warranty,
            customer=customer,
            _quantity=5,
        )

        response = api_client.get("/warranty/request/all/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5  # noqa: PLR2004

    def test_if_customer_can_get_warranty_request_detail_return_200(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)
        warranty_request = baker.make(
            WarrantyRequest,
            customer=customer,
            warranty=warranty,
        )
        response = api_client.get(f"/warranty/request/{warranty_request.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(warranty_request.id)

    def test_if_customer_cannot_get_other_warranty_request_detail_return_400(
        self,
        api_client,
        make_customer,
    ):
        customer1 = make_customer()
        customer2 = make_customer()
        api_client.force_authenticate(user=customer1.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer2, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer2, orderitem=orderitem)
        warranty_request = baker.make(
            WarrantyRequest,
            customer=customer2,
            warranty=warranty,
        )
        response = api_client.get(f"/warranty/request/{warranty_request.id}/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_anonymous_user_cannot_create_warranty_request_return_403(
        self,
        api_client,
    ):
        response = api_client.post("/warranty/request/create/", {})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_customer_can_create_warranty_request_return_201(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)
        data = {"warranty_id": str(warranty.id), "description": "Keyboard not working"}
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert WarrantyRequest.objects.filter(id=response.data["id"]).exists()

    def test_if_customer_cannot_create_warranty_request_for_other_warranty_return_400(
        self,
        api_client,
        make_customer,
    ):
        customer1 = make_customer()
        customer2 = make_customer()
        api_client.force_authenticate(user=customer1.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer2, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer2, orderitem=orderitem)
        data = {"warranty_id": str(warranty.id), "description": "Test"}
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_product_manager_can_approve_warranty_request_return_200(
        self,
        api_client,
        make_customer,
        make_employee_is_product_manager,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, orderitem=orderitem, customer=customer)
        warranty_request = baker.make(
            WarrantyRequest,
            warranty=warranty,
            customer=customer,
        )

        response = api_client.post(
            f"/warranty/request/{warranty_request.id}/approve/",
            {"note": "Approved"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_product_manager_can_reject_warranty_request_return_200(
        self,
        api_client,
        make_employee_is_product_manager,
        make_customer,
    ):
        product_manager = make_employee_is_product_manager()
        customer = make_customer(auth=False)
        api_client.force_authenticate(user=product_manager)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)

        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        warranty = baker.make(Warranty, orderitem=orderitem, customer=customer)
        warranty_request = baker.make(
            WarrantyRequest,
            warranty=warranty,
            customer=customer,
        )

        response = api_client.post(
            f"/warranty/request/{warranty_request.id}/reject/",
            {"note": "Rejected due to damage"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_invalid_warranty_id_in_create_request_return_400(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        data = {
            "warranty_id": "123e4567-e89b-12d3-a456-426614174000",
            "description": "Test",
        }
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_missing_description_in_create_request_return_400(
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)
        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)
        orderitem = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )
        warranty = baker.make(Warranty, customer=customer, orderitem=orderitem)
        data = {"warranty_id": str(warranty.id)}
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_customer_cannot_create_request_for_expired_or_voided_warranty_return_400(  # noqa: E501
        self,
        api_client,
        make_customer,
    ):
        customer = make_customer()
        api_client.force_authenticate(user=customer.user)

        product = baker.make(Kit, name="Test Product")
        content_type = ContentType.objects.get_for_model(Kit)
        order = baker.make(Order, customer=customer, status=OrderStatus.DELIVERED)

        # OrderItem 1 → cho expired warranty
        orderitem_1 = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        expired_warranty = baker.make(
            Warranty,
            customer=customer,
            orderitem=orderitem_1,
            status=Warranty.Status.EXPIRED,
        )
        data = {"warranty_id": str(expired_warranty.id), "description": "Expired test"}
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # OrderItem 2 → cho void warranty
        orderitem_2 = baker.make(
            OrderItem,
            order=order,
            content_type=content_type,
            object_id=product.id,
            name_snapshot=product.name,
            price_snapshot=100.00,
        )

        void_warranty = baker.make(
            Warranty,
            customer=customer,
            orderitem=orderitem_2,
            status=Warranty.Status.VOIDED,
        )
        data = {"warranty_id": str(void_warranty.id), "description": "Void test"}
        response = api_client.post("/warranty/request/create/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
