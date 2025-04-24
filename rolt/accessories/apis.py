from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rolt.accessories.models import Accessory
from rolt.accessories.selectors import accessory_get
from rolt.accessories.selectors import accessory_list
from rolt.accessories.services import AccessoryData
from rolt.accessories.services import accessory_create
from rolt.accessories.services import accessory_delete
from rolt.accessories.services import accessory_update
from rolt.common.pagination import LimitOffsetPagination
from rolt.common.pagination import get_paginated_response
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class AccessoryListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "accessory_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        type = serializers.CharField(required=False)
        price_min = serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            required=False,
        )
        price_max = serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
            required=False,
        )

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Accessory
            fields = "__all__"

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        accessories = accessory_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=accessories,
            request=request,
            view=self,
        )


class AccessoryDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "accessory_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Accessory
            fields = "__all__"

    def get(self, request, pk):
        accessory = accessory_get(id=pk)
        if not accessory:
            msg = "Accessory not found"
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(accessory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccessoryCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "accessory_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Accessory
            fields = "__all__"

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        accessory_data = AccessoryData(**serializer.validated_data)
        accessory = accessory_create(data=accessory_data)
        return Response({"id": accessory.id}, status=status.HTTP_201_CREATED)


class AccessoryUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "accessory_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Accessory
            fields = "__all__"

    def patch(self, request, pk):
        accessory = accessory_get(id=pk)
        if not accessory:
            msg = "Accessory not found"
            raise ApplicationError(msg)

        serializer = self.InputSerializer(
            instance=accessory,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        accessory = accessory_update(instance=accessory, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class AccessoryDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "accessory_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, pk):
        accessory = accessory_get(id=pk)
        if not accessory:
            msg = "Accessory not found"
            raise ApplicationError(msg)
        accessory_delete(instance=accessory)
        return Response(status=status.HTTP_204_NO_CONTENT)
