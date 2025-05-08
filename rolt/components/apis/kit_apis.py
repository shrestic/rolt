from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rolt.common.pagination import LimitOffsetPagination
from rolt.common.pagination import get_paginated_response
from rolt.common.utils import inline_serializer
from rolt.components.models.kit_model import Kit
from rolt.components.selectors.kit_selectors import kit_get
from rolt.components.selectors.kit_selectors import kit_get_existing_codes
from rolt.components.selectors.kit_selectors import kit_list
from rolt.components.services.kit_services import KitData
from rolt.components.services.kit_services import kit_bulk_create
from rolt.components.services.kit_services import kit_create
from rolt.components.services.kit_services import kit_delete
from rolt.components.services.kit_services import kit_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager
from rolt.manufacturers.services import manufacturer_get
from rolt.manufacturers.services import manufacturer_get_dict_by_codes


class KitListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "kit_list"  # 100/hour from LIST_RATE

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        number_of_keys = serializers.IntegerField(required=False)
        layout = serializers.CharField(required=False)
        layout_detail = serializers.CharField(required=False)
        case_spec = serializers.CharField(required=False)
        mounting_style = serializers.CharField(required=False)
        plate_material = serializers.CharField(required=False)
        stab_mount = serializers.CharField(required=False)
        firmware_type = serializers.CharField(required=False)
        connectivity = serializers.CharField(required=False)
        rgb_type = serializers.CharField(required=False)
        manufacturer = serializers.CharField(required=False)
        manufacturer_code = serializers.CharField(required=False)
        hot_swap = serializers.BooleanField(required=False, allow_null=True)
        knob = serializers.BooleanField(required=False, allow_null=True)
        price_min = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
            allow_null=True,
        )
        price_max = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
            allow_null=True,
        )

    class OutputSerializer(serializers.ModelSerializer):
        manufacturer = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )

        class Meta:
            model = Kit
            fields = "__all__"

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        kits = kit_list(filters=filters_serializer.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=kits,
            request=request,
            view=self,
        )


class KitDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "kit_detail"  # 200/hour from DETAIL_RATE

    class OutputSerializer(serializers.ModelSerializer):
        manufacturer = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )

        class Meta:
            model = Kit
            fields = "__all__"

    def get(self, request, code):
        kit = kit_get(code=code)
        if not kit:
            msg = "Keyboard kit not found"
            raise ApplicationError(message=msg)
        serializer = self.OutputSerializer(kit)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KitCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "kit_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Kit
            exclude = ("manufacturer",)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code", None)
        if kit_get(code=code):
            msg = f"Keyboard kit with code {code} already exists"
            raise ApplicationError(message=msg)
        manufacturer = manufacturer_get(
            code=serializer.validated_data.pop("manufacturer_code"),
        )
        if not manufacturer:
            msg = "Manufacturer not found"
            raise ApplicationError(message=msg)

        kit_data = KitData(
            manufacturer=manufacturer,
            **serializer.validated_data,
        )

        kit = kit_create(data=kit_data)
        return Response({"code": kit.code}, status=status.HTTP_201_CREATED)


class KitUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "kit_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.IntegerField(required=False)

        class Meta:
            model = Kit
            exclude = ("manufacturer",)

    def patch(self, request, code):
        kit = kit_get(code=code)
        if not kit:
            msg = "Keyboard kit not found"
            raise ApplicationError(message=msg)

        serializer = self.InputSerializer(kit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        manufacturer_code = serializer.validated_data.pop("manufacturer_code", None)
        if manufacturer_code:
            manufacturer = manufacturer_get(code=manufacturer_code)
            if not manufacturer:
                msg = "Manufacturer not found"
                raise ApplicationError(message=msg)
            serializer.validated_data["manufacturer"] = manufacturer
        kit_update(instance=kit, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class KitDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "kit_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, code):
        kit = kit_get(code=code)
        if not kit:
            msg = "Keyboard kit not found"
            raise ApplicationError(message=msg)
        kit_delete(instance=kit)
        return Response(status=status.HTTP_204_NO_CONTENT)


class KitBulkCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "kit_bulk_create"  # 50/hour from BULK_CREATE_RATE

    class InputSerializer(serializers.ModelSerializer):
        manufacturer_code = serializers.CharField()

        class Meta:
            model = Kit
            exclude = ("manufacturer",)

    def post(self, request):
        if not isinstance(request.data, list):
            msg = "Expected a list of keyboard kits"
            raise ApplicationError(message=msg)

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        kits = []

        manufacturer_codes = [
            item["manufacturer_code"] for item in serializer.validated_data
        ]
        codes = [item["code"] for item in serializer.validated_data]

        # Get existing codes from DB
        existing_codes = kit_get_existing_codes(codes=codes)
        if existing_codes:
            msg = (
                f"Keyboard kit with code(s) {', '.join(existing_codes)} already exist."
            )
            raise ApplicationError(message=msg)

        # Get manufacturers
        manufacturer_dict = manufacturer_get_dict_by_codes(manufacturer_codes)

        for item in serializer.validated_data:
            manufacturer_code = item.pop("manufacturer_code")
            manufacturer = manufacturer_dict.get(manufacturer_code)
            if not manufacturer:
                msg = f"Manufacturer with code {manufacturer_code} not found"
                raise ApplicationError(message=msg)
            kits.append(Kit(manufacturer=manufacturer, **item))

        created_kits = kit_bulk_create(kits=kits)
        return Response(
            [kit.code for kit in created_kits],
            status=status.HTTP_201_CREATED,
        )
