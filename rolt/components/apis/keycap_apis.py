from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rolt.common.pagination import LimitOffsetPagination
from rolt.common.pagination import get_paginated_response
from rolt.common.utils import inline_serializer
from rolt.components.models.keycap_model import Keycap
from rolt.components.selectors.keycap_selectors import keycap_get
from rolt.components.selectors.keycap_selectors import keycap_get_existing_codes
from rolt.components.selectors.keycap_selectors import keycap_list
from rolt.components.services.keycap_services import KeycapData
from rolt.components.services.keycap_services import keycap_bulk_create
from rolt.components.services.keycap_services import keycap_create
from rolt.components.services.keycap_services import keycap_delete
from rolt.components.services.keycap_services import keycap_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager
from rolt.manufacturers.services import manufacturer_get
from rolt.manufacturers.services import manufacturer_get_dict_by_codes


class KeycapListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "keycap_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        material = serializers.CharField(required=False)
        profile = serializers.CharField(required=False)
        legend_type = serializers.CharField(required=False)
        compatibility = serializers.CharField(required=False)
        layout_support = serializers.CharField(required=False)
        colorway = serializers.CharField(required=False)
        theme_name = serializers.CharField(required=False)
        texture = serializers.CharField(required=False)
        sound_profile = serializers.CharField(required=False)
        manufacturer = serializers.CharField(required=False)
        manufacturer_code = serializers.CharField(required=False)
        shine_through = serializers.BooleanField(required=False, allow_null=True)
        number_of_keys_min = serializers.IntegerField(required=False)
        number_of_keys_max = serializers.IntegerField(required=False)
        thickness_min = serializers.FloatField(required=False)
        thickness_max = serializers.FloatField(required=False)
        price_min = serializers.IntegerField(required=False)
        price_max = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        manufacturer = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )

        class Meta:
            model = Keycap
            fields = "__all__"

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        keycaps = keycap_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=keycaps,
            request=request,
            view=self,
        )


class KeycapDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "keycap_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        manufacturer = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )

        class Meta:
            model = Keycap
            fields = "__all__"

    def get(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Keycap not found")
        serializer = self.OutputSerializer(keycap)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeycapCreateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Keycap
            exclude = ("manufacturer",)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")
        if keycap_get(code=code):
            raise ApplicationError(message=f"Keycap with code {code} already exists")

        manufacturer = manufacturer_get(
            code=serializer.validated_data.pop("manufacturer_code"),
        )
        if not manufacturer:
            raise ApplicationError(message="Manufacturer not found")

        keycap_data = KeycapData(manufacturer=manufacturer, **serializer.validated_data)
        keycap = keycap_create(data=keycap_data)
        return Response({"code": keycap.code}, status=status.HTTP_201_CREATED)


class KeycapUpdateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField(required=False)

        class Meta:
            model = Keycap
            exclude = ("manufacturer",)

    def patch(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Keycap not found")

        serializer = self.InputSerializer(keycap, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        manufacturer_code = serializer.validated_data.pop("manufacturer_code", None)
        if manufacturer_code:
            manufacturer = manufacturer_get(code=manufacturer_code)
            if not manufacturer:
                raise ApplicationError(message="Manufacturer not found")
            serializer.validated_data["manufacturer"] = manufacturer

        keycap = keycap_update(instance=keycap, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class KeycapDeleteApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Keycap not found")
        keycap_delete(instance=keycap)
        return Response(status=status.HTTP_204_NO_CONTENT)


class KeycapBulkCreateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_bulk_create"  # 50/hour from BULK_CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Keycap
            exclude = ("manufacturer",)

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(message="Expected a list of keycaps")

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        manufacturer_codes = [
            item["manufacturer_code"] for item in serializer.validated_data
        ]
        codes = [item["code"] for item in serializer.validated_data]

        existing_codes = keycap_get_existing_codes(codes=codes)
        if existing_codes:
            msg = f"Keycap with code(s) {', '.join(existing_codes)} already exist."
            raise ApplicationError(message=msg)

        manufacturer_dict = manufacturer_get_dict_by_codes(manufacturer_codes)
        keycaps = []

        for item in serializer.validated_data:
            manufacturer_code = item.pop("manufacturer_code")
            manufacturer = manufacturer_dict.get(manufacturer_code)
            if not manufacturer:
                raise ApplicationError(
                    message=f"Manufacturer with code {manufacturer_code} not found",
                )
            keycaps.append(Keycap(manufacturer=manufacturer, **item))

        created_keycaps = keycap_bulk_create(keycaps=keycaps)
        return Response(
            [keycap.code for keycap in created_keycaps],
            status=status.HTTP_201_CREATED,
        )
