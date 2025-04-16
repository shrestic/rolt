from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.brand.services import brand_get
from rolt.brand.services import brand_get_dict_by_codes
from rolt.common.pagination import LimitOffsetPagination
from rolt.common.utils import inline_serializer
from rolt.component_types.services import component_type_get
from rolt.component_types.services import component_type_get_dict_by_codes
from rolt.components.models.switch_model import Switch
from rolt.components.selectors.switch_selector import switch_check_type_and_brand
from rolt.components.selectors.switch_selector import switch_get
from rolt.components.selectors.switch_selector import switch_list
from rolt.components.services.switch_service import switch_bulk_create
from rolt.components.services.switch_service import switch_create
from rolt.components.services.switch_service import switch_delete
from rolt.components.services.switch_service import switch_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class SwitchListApi(APIView):
    permission_classes = [AllowAny]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        label = serializers.CharField(required=False)
        brand = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        type = serializers.CharField(required=False)
        type_code = serializers.CharField(required=False)

        is_lubed = serializers.BooleanField(required=False)

        price_min = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
        )
        price_max = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
        )

    class OutputSerializer(serializers.ModelSerializer):
        brand = inline_serializer(
            fields={
                "code": serializers.CharField(required=False),
                "label": serializers.CharField(required=False),
                "logo": serializers.ImageField(required=False),
            },
        )
        type = inline_serializer(
            fields={
                "code": serializers.CharField(required=False),
                "label": serializers.CharField(required=False),
                "applies_to": serializers.CharField(required=False),
                "note": serializers.CharField(required=False),
            },
        )

        class Meta:
            model = Switch
            fields = [
                "code",
                "label",
                "brand",
                "is_lubed",
                "type",
                "description",
                "price",
                "image",
            ]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        switches = switch_list(
            filters=filters_serializer.validated_data,
        )
        serializer = self.OutputSerializer(switches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwitchDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        brand = inline_serializer(
            fields={
                "code": serializers.CharField(required=False),
                "label": serializers.CharField(required=False),
                "logo": serializers.ImageField(required=False),
            },
        )
        type = inline_serializer(
            fields={
                "code": serializers.CharField(required=False),
                "label": serializers.CharField(required=False),
                "applies_to": serializers.CharField(required=False),
                "note": serializers.CharField(required=False),
            },
        )

        class Meta:
            model = Switch
            fields = [
                "code",
                "label",
                "brand",
                "is_lubed",
                "type",
                "description",
                "price",
                "image",
            ]

    def get(self, request, code):
        switch = Switch.objects.get(code=code)
        serializer = self.OutputSerializer(switch)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwitchCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        type_code = serializers.CharField()
        is_lubed = serializers.BooleanField()
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand_code = serializer.validated_data["brand_code"]
        brand = brand_get(code=brand_code)
        if not brand:
            raise ApplicationError(
                message="Brand with this code does not exist.",
            )
        type_code = serializer.validated_data["type_code"]
        type = component_type_get(code=type_code)  # noqa: A001
        if not type:
            raise ApplicationError(
                message="Component type with this code does not exist.",
            )
        existed_switch = switch_get(
            code=serializer.validated_data["code"],
        )
        if existed_switch:
            raise ApplicationError(
                message="Switch with this code already exists.",
            )
        is_same_component_type_and_brand = switch_check_type_and_brand(
            brand=brand,
            type=type,
        )
        if is_same_component_type_and_brand:
            raise ApplicationError(
                message="Switch with this brand and component type already exists.",
            )
        switch = switch_create(
            code=serializer.validated_data["code"],
            label=serializer.validated_data["label"],
            brand=brand,
            type=type,
            is_lubed=serializer.validated_data["is_lubed"],
            description=serializer.validated_data["description"],
            price=serializer.validated_data["price"],
            image=serializer.validated_data.get("image"),
        )

        return Response(switch.code, status=status.HTTP_201_CREATED)


class SwitchUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        label = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        type_code = serializers.CharField(required=False)
        is_lubed = serializers.BooleanField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
        )
        image = serializers.ImageField(required=False, allow_null=True)

        class Meta:
            model = Switch
            fields = [
                "label",
                "brand_code",
                "type_code",
                "is_lubed",
                "description",
                "price",
                "image",
            ]

    def patch(self, request, code):
        switch = switch_get(code=code)
        if not switch:
            raise ApplicationError(
                message="Switch with this code does not exist.",
            )

        serializer = self.InputSerializer(switch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        brand_code = serializer.validated_data.pop("brand_code", None)
        type_code = serializer.validated_data.pop("type_code", None)

        brand = None
        type = None  # noqa: A001

        if brand_code:
            brand = brand_get(code=brand_code)
            if not brand:
                raise ApplicationError(
                    message="Brand with this code does not exist.",
                )
            serializer.validated_data["brand"] = brand

        if type_code:
            type = component_type_get(code=type_code)  # noqa: A001
            if not type:
                raise ApplicationError(
                    message="Component type with this code does not exist.",
                )
            serializer.validated_data["type"] = type
        # Check if the switch with the same brand and type already exists
        if brand and type:
            is_same_component_type_and_brand = switch_check_type_and_brand(
                brand=brand,
                type=type,
            )
            if is_same_component_type_and_brand:
                raise ApplicationError(
                    message="Switch with this brand and component type already exists.",
                )

        switch = switch_update(instance=switch, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class SwitchDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        switch = switch_get(code=code)
        if not switch:
            raise ApplicationError(
                message="Switch with this code does not exist.",
            )
        switch_delete(instance=switch)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwitchBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        type_code = serializers.CharField()
        is_lubed = serializers.BooleanField()
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Switch
            fields = "__all__"

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(message="Expected a list of switch.")

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Get all unique brand_codes & type_codes
        brand_codes = [item["brand_code"] for item in data]
        type_codes = [item["type_code"] for item in data]

        # Use in_bulk
        brand_dict = brand_get_dict_by_codes(brand_codes)
        type_dict = component_type_get_dict_by_codes(type_codes)

        switches = []

        for item in data:
            code = item["code"]

            # Check duplicate code
            if switch_get(code=code):
                msg = f"Switch with code '{code}' already exists."
                raise ApplicationError(msg)

            # Validate brand
            brand = brand_dict.get(item["brand_code"])
            if not brand:
                msg = f"Brand with code '{item['brand_code']}' does not exist."
                raise ApplicationError(msg)

            # Validate component type
            type = type_dict.get(item["type_code"])  # noqa: A001
            if not type:
                msg = f"ComponentType with code '{item['type_code']}' does not exist."
                raise ApplicationError(msg)

            # Check uniqueness combo
            exists_combo = switch_check_type_and_brand(
                brand=brand,
                type=type,
            )
            if exists_combo:
                msg = f"Switch with brand '{brand.code}' and type '{type.code}' already exists."  # noqa: E501
                raise ApplicationError(msg)

            switches.append(
                Switch(
                    code=code,
                    label=item["label"],
                    brand=brand,
                    type=type,
                    is_lubed=item["is_lubed"],
                    description=item["description"],
                    price=item["price"],
                    image=item["image"],
                ),
            )

        created_switches = switch_bulk_create(switches=switches)
        output = self.OutputSerializer(created_switches, many=True)
        return Response(output.data, status=status.HTTP_201_CREATED)
