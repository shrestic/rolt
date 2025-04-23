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
from rolt.components.models.switch_model import Switch
from rolt.components.selectors.switch_selectors import switch_get
from rolt.components.selectors.switch_selectors import switch_get_existing_codes
from rolt.components.selectors.switch_selectors import switch_list
from rolt.components.services.switch_services import SwitchData
from rolt.components.services.switch_services import switch_bulk_create
from rolt.components.services.switch_services import switch_create
from rolt.components.services.switch_services import switch_delete
from rolt.components.services.switch_services import switch_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager
from rolt.manufacturers.services import manufacturer_get
from rolt.manufacturers.services import manufacturer_get_dict_by_codes


class SwitchListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "switch_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        type = serializers.CharField(required=False)
        sound_level = serializers.CharField(required=False)
        stem_material = serializers.CharField(required=False)
        housing_material = serializers.CharField(required=False)
        pin_type = serializers.CharField(required=False)
        compatible_with = serializers.CharField(required=False)
        manufacturer = serializers.CharField(required=False)
        manufacturer_code = serializers.CharField(required=False)
        factory_lubed = serializers.BooleanField(required=False, allow_null=True)
        led_support = serializers.BooleanField(required=False, allow_null=True)
        actuation_force_min = serializers.IntegerField(required=False)
        actuation_force_max = serializers.IntegerField(required=False)
        bottom_out_force_min = serializers.IntegerField(required=False)
        bottom_out_force_max = serializers.IntegerField(required=False)
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
            model = Switch
            fields = "__all__"

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        switches = switch_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=switches,
            request=request,
            view=self,
        )


class SwitchDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "switch_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        manufacturer = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )

        class Meta:
            model = Switch
            fields = "__all__"

    def get(self, request, code):
        switch = switch_get(code=code)
        if not switch:
            raise ApplicationError(message="Switch not found")
        serializer = self.OutputSerializer(switch)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwitchCreateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "switch_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Switch
            exclude = ("manufacturer",)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")
        if switch_get(code=code):
            raise ApplicationError(message=f"Switch with code {code} already exists")

        manufacturer = manufacturer_get(
            code=serializer.validated_data.pop("manufacturer_code"),
        )
        if not manufacturer:
            raise ApplicationError(message="Manufacturer not found")

        switch_data = SwitchData(
            manufacturer=manufacturer,
            **serializer.validated_data,
        )
        switch = switch_create(data=switch_data)
        return Response({"code": switch.code}, status=status.HTTP_201_CREATED)


class SwitchUpdateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "switch_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField(required=False)

        class Meta:
            model = Switch
            exclude = ("manufacturer",)

    def patch(self, request, code):
        switch = switch_get(code=code)
        if not switch:
            raise ApplicationError(message="Switch not found")

        serializer = self.InputSerializer(switch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        manufacturer_code = serializer.validated_data.pop("manufacturer_code", None)
        if manufacturer_code:
            manufacturer = manufacturer_get(code=manufacturer_code)
            if not manufacturer:
                raise ApplicationError(message="Manufacturer not found")
            serializer.validated_data["manufacturer"] = manufacturer

        switch = switch_update(instance=switch, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class SwitchDeleteApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "switch_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, code):
        switch = switch_get(code=code)
        if not switch:
            raise ApplicationError(message="Switch not found")
        switch_delete(instance=switch)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwitchBulkCreateApi(APIView):
    permission_classes = [IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "switch_bulk_create"  # 50/hour from BULK_CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Switch
            exclude = ("manufacturer",)

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(message="Expected a list of switches")

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        manufacturer_codes = [
            item["manufacturer_code"] for item in serializer.validated_data
        ]
        codes = [item["code"] for item in serializer.validated_data]

        existing_codes = switch_get_existing_codes(codes=codes)
        if existing_codes:
            msg = f"Switch with code(s) {', '.join(existing_codes)} already exist."
            raise ApplicationError(message=msg)

        manufacturer_dict = manufacturer_get_dict_by_codes(manufacturer_codes)
        switches = []

        for item in serializer.validated_data:
            manufacturer_code = item.pop("manufacturer_code")
            manufacturer = manufacturer_dict.get(manufacturer_code)
            if not manufacturer:
                raise ApplicationError(
                    message=f"Manufacturer with code {manufacturer_code} not found",
                )
            switches.append(Switch(manufacturer=manufacturer, **item))

        created_switches = switch_bulk_create(switches=switches)
        return Response(
            [switch.code for switch in created_switches],
            status=status.HTTP_201_CREATED,
        )
