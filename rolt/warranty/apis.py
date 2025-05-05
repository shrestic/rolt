from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.common.pagination import LimitOffsetPagination
from rolt.common.pagination import get_paginated_response
from rolt.common.utils import inline_serializer
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.core.permissions import IsProductManager
from rolt.warranty.models import Warranty
from rolt.warranty.models import WarrantyRequest
from rolt.warranty.selectors import warranty_get
from rolt.warranty.selectors import warranty_list_by_customer
from rolt.warranty.selectors import warranty_request_get
from rolt.warranty.selectors import warranty_request_list_all
from rolt.warranty.selectors import warranty_request_list_by_customer
from rolt.warranty.services import warranty_delete
from rolt.warranty.services import warranty_mark_expired
from rolt.warranty.services import warranty_request_approve
from rolt.warranty.services import warranty_request_create
from rolt.warranty.services import warranty_request_reject
from rolt.warranty.services import warranty_void


class WarrantyListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.ModelSerializer):
        orderitem = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "product_name": serializers.CharField(source="product.name"),
            },
        )

        class Meta:
            model = Warranty
            fields = [
                "id",
                "orderitem",
                "start_date",
                "end_date",
                "status",
                "notes",
            ]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        warranties = warranty_list_by_customer(customer=customer)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=warranties,
            request=request,
            view=self,
        )


class WarrantyDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        orderitem = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "product_name": serializers.CharField(source="product.name"),
            },
        )

        class Meta:
            model = Warranty
            fields = [
                "id",
                "orderitem",
                "start_date",
                "end_date",
                "status",
                "notes",
            ]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        warranty = warranty_get(id=pk)
        if not warranty or warranty.customer != customer:
            raise ApplicationError(message="Warranty not found or not owned by you")
        serializer = self.OutputSerializer(warranty)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WarrantyVoidApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_update"  # 50/hour from UPDATE_RATE

    class InputSerializer(serializers.Serializer):
        note = serializers.CharField(required=False, allow_blank=True)

    def post(self, request, pk):
        warranty = warranty_get(id=pk)
        if not warranty:
            raise ApplicationError(message="Warranty not found")

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        warranty = warranty_void(instance=warranty, note=data.get("note", ""))
        return Response(status=status.HTTP_200_OK)


class WarrantyMarkExpiredApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_update"  # 50/hour from UPDATE_RATE

    def post(self, request, pk):
        warranty = warranty_get(id=pk)
        if not warranty:
            raise ApplicationError(message="Warranty not found")

        warranty = warranty_mark_expired(instance=warranty)
        return Response(status=status.HTTP_200_OK)


class WarrantyRequestListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.ModelSerializer):
        warranty = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "orderitem": inline_serializer(
                    fields={
                        "id": serializers.UUIDField(),
                        "product_name": serializers.CharField(source="product.name"),
                    },
                ),
            },
        )

        class Meta:
            model = WarrantyRequest
            fields = [
                "id",
                "warranty",
                "description",
                "status",
                "admin_notes",
                "created_at",
            ]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        warranty_requests = warranty_request_list_by_customer(customer=customer)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=warranty_requests,
            request=request,
            view=self,
        )


class WarrantyRequestAllListApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.ModelSerializer):
        warranty = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "orderitem": inline_serializer(
                    fields={
                        "id": serializers.UUIDField(),
                        "product_name": serializers.CharField(source="product.name"),
                    },
                ),
            },
        )
        customer = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "email": serializers.EmailField(source="user.email"),
            },
        )

        class Meta:
            model = WarrantyRequest
            fields = [
                "id",
                "warranty",
                "customer",
                "description",
                "status",
                "admin_notes",
                "created_at",
            ]

    def get(self, request):
        warranty_requests = warranty_request_list_all()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=warranty_requests,
            request=request,
            view=self,
        )


class WarrantyRequestDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        warranty = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "orderitem": inline_serializer(
                    fields={
                        "id": serializers.UUIDField(),
                        "product_name": serializers.CharField(source="product.name"),
                    },
                ),
            },
        )

        class Meta:
            model = WarrantyRequest
            fields = [
                "id",
                "warranty",
                "description",
                "status",
                "admin_notes",
                "created_at",
            ]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        warranty_request = warranty_request_get(id=pk)
        if not warranty_request or warranty_request.customer != customer:
            raise ApplicationError(
                message="Warranty request not found or not owned by you",
            )
        serializer = self.OutputSerializer(warranty_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WarrantyRequestCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.Serializer):
        warranty_id = serializers.UUIDField()
        description = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")

        warranty = warranty_get(id=data["warranty_id"])
        if not warranty:
            raise ApplicationError(message="Warranty not found")
        if warranty.status != Warranty.Status.ACTIVE:
            raise ApplicationError(message="Warranty is not active or already voided")
        if warranty.customer != customer:
            raise ApplicationError(message="Warranty not owned by you")

        warranty_request = warranty_request_create(
            warranty=warranty,
            customer=customer,
            description=data["description"],
        )
        return Response({"id": warranty_request.id}, status=status.HTTP_201_CREATED)


class WarrantyRequestApproveApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_update"  # 50/hour from UPDATE_RATE

    class InputSerializer(serializers.Serializer):
        note = serializers.CharField(required=False, allow_blank=True)

    def post(self, request, pk):
        warranty_request = warranty_request_get(id=pk)
        if not warranty_request:
            raise ApplicationError(message="Warranty request not found")

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        warranty_request_approve(
            instance=warranty_request,
            note=data.get("note", ""),
        )
        return Response(status=status.HTTP_200_OK)


class WarrantyRequestRejectApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_request_update"  # 50/hour from UPDATE_RATE

    class InputSerializer(serializers.Serializer):
        note = serializers.CharField(required=False, allow_blank=True)

    def post(self, request, pk):
        warranty_request = warranty_request_get(id=pk)
        if not warranty_request:
            raise ApplicationError(message="Warranty request not found")

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        warranty_request_reject(
            instance=warranty_request,
            note=data.get("note", ""),
        )
        return Response(status=status.HTTP_200_OK)


class WarrantyDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "warranty_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, pk):
        warranty = warranty_get(id=pk)
        if not warranty:
            raise ApplicationError(message="Warranty not found")
        warranty_delete(instance=warranty)
        return Response(status=status.HTTP_204_NO_CONTENT)
