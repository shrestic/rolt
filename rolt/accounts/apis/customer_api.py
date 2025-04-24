from rest_framework import serializers
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.models.customer_model import Customer
from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.accounts.services.customer_service import CustomerService
from rolt.common.pagination import get_paginated_response
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.core.permissions import IsSupportStaff
from rolt.users.serializers import UserSerializer


class MeCustomerDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Customer
            fields = ["phone", "address", "birth_date", "image", "user"]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)

        if customer is None:
            raise ApplicationError(message="Customer not found")
        output_serializer = self.OutputSerializer(customer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class MeCustomerUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        birth_date = serializers.DateField(required=False)
        image = serializers.ImageField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ["phone", "address", "birth_date", "image"]

    def patch(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        customer = CustomerService().customer_update(
            data=input_serializer.validated_data,
            customer=customer,
        )
        output_serializer = self.OutputSerializer(customer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class AdminCustomerListApi(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=False)
        is_staff = serializers.BooleanField(
            required=False,
            allow_null=True,
            default=None,
        )
        is_active = serializers.BooleanField(
            required=False,
            allow_null=True,
            default=None,
        )
        email = serializers.EmailField(required=False)
        phone = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        birth_date_after = serializers.DateField(required=False)
        birth_date_before = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Customer
            fields = ["phone", "address", "birth_date", "image", "user"]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = CustomerSelector().customer_list(
            filters=filters_serializer.validated_data,
        )

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )


class AdminCustomerDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Customer
            fields = ["phone", "address", "birth_date", "image", "user"]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(pk=pk)

        if customer is None:
            raise ApplicationError(message="Customer not found")
        output_serializer = self.OutputSerializer(customer)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
