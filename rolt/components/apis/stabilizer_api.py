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
from rolt.components.models.stabilizer_model import Stabilizer
from rolt.components.selectors.stabilizer_selector import (
    stabilizer_check_mount_and_brand,
)
from rolt.components.selectors.stabilizer_selector import stabilizer_get
from rolt.components.selectors.stabilizer_selector import stabilizer_list
from rolt.components.services.stabilizer_service import stabilizer_bulk_create
from rolt.components.services.stabilizer_service import stabilizer_create
from rolt.components.services.stabilizer_service import stabilizer_delete
from rolt.components.services.stabilizer_service import stabilizer_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class StabilizerListApi(APIView):
    permission_classes = [AllowAny]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        label = serializers.CharField(required=False)
        brand = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        mount = serializers.CharField(required=False)
        mount_code = serializers.CharField(required=False)
        is_lubed = serializers.BooleanField(required=False, allow_null=True)

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
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )
        mount = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Stabilizer
            fields = [
                "code",
                "label",
                "brand",
                "mount",
                "is_lubed",
                "price",
                "image",
                "description",
            ]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        stabilizers = stabilizer_list(filters=filters_serializer.validated_data)
        serializer = self.OutputSerializer(stabilizers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StabilizerDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        brand = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )
        mount = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Stabilizer
            fields = [
                "code",
                "label",
                "brand",
                "mount",
                "is_lubed",
                "price",
                "image",
                "description",
            ]

    def get(self, request, code):
        stabilizer = stabilizer_get(code=code)
        if not stabilizer:
            msg = "Stabilizer with this code does not exist."
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(stabilizer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StabilizerCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        mount_code = serializers.CharField()
        is_lubed = serializers.BooleanField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand = brand_get(code=serializer.validated_data["brand_code"])
        if not brand:
            msg = "Brand with this code does not exist."
            raise ApplicationError(msg)
        mount = component_type_get(
            code=serializer.validated_data["mount_code"],
        )
        if not mount:
            msg = "Component type with this code does not exist."
            raise ApplicationError(msg)
        if stabilizer_get(code=serializer.validated_data["code"]):
            msg = "Stabilizer with this code already exists."
            raise ApplicationError(msg)
        if stabilizer_check_mount_and_brand(brand=brand, mount=mount):
            msg = "Stabilizer with this brand and mount type already exists."
            raise ApplicationError(msg)
        stabilizer = stabilizer_create(
            code=serializer.validated_data["code"],
            label=serializer.validated_data["label"],
            brand=brand,
            mount=mount,
            is_lubed=serializer.validated_data["is_lubed"],
            price=serializer.validated_data["price"],
            image=serializer.validated_data.get("image"),
            description=serializer.validated_data.get("description", ""),
        )
        return Response(stabilizer.code, status=status.HTTP_201_CREATED)


class StabilizerUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        label = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        mount_code = serializers.CharField(required=False)
        is_lubed = serializers.BooleanField(required=False)
        price = serializers.DecimalField(
            required=False,
            max_digits=10,
            decimal_places=2,
        )
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

        class Meta:
            model = Stabilizer
            fields = [
                "label",
                "brand_code",
                "mount_code",
                "is_lubed",
                "price",
                "image",
                "description",
            ]

    def patch(self, request, code):
        stabilizer = stabilizer_get(code=code)
        if not stabilizer:
            msg = "Stabilizer with this code does not exist."
            raise ApplicationError(msg)
        serializer = self.InputSerializer(stabilizer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        brand_code = serializer.validated_data.pop("brand_code", None)
        mount_code = serializer.validated_data.pop("mount_code", None)

        brand = None
        mount = None

        if brand_code:
            brand = brand_get(code=brand_code)
            if not brand:
                raise ApplicationError(
                    message="Brand with this code does not exist.",
                )
            serializer.validated_data["brand"] = brand

        if mount_code:
            mount = component_type_get(code=mount_code)
            if not mount:
                raise ApplicationError(
                    message="Mount type with this code does not exist.",
                )
            serializer.validated_data["type"] = mount
        # Check if the stabilizer with the same brand and mount type already exists
        if brand and mount:
            is_same_mount_and_brand = stabilizer_check_mount_and_brand(
                brand=brand,
                mount=mount,
            )
            if is_same_mount_and_brand:
                raise ApplicationError(
                    message="Stabilizer with this brand and mount type already exists.",
                )
        stabilizer = stabilizer_update(
            instance=stabilizer,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)


class StabilizerDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        stabilizer = stabilizer_get(code=code)
        if not stabilizer:
            msg = "Stabilizer with this code does not exist."
            raise ApplicationError(msg)
        stabilizer_delete(instance=stabilizer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StabilizerBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        mount_code = serializers.CharField()
        is_lubed = serializers.BooleanField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Stabilizer
            fields = "__all__"

    def post(self, request):
        if not isinstance(request.data, list):
            msg = "Expected a list of stabilizers."
            raise ApplicationError(msg)

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        brand_codes = [item["brand_code"] for item in data]
        mount_codes = [item["mount_code"] for item in data]

        brand_dict = brand_get_dict_by_codes(brand_codes)
        mount_dict = component_type_get_dict_by_codes(mount_codes)

        stabilizers = []
        for item in data:
            if stabilizer_get(code=item["code"]):
                msg = f"Stabilizer with code '{item['code']}' already exists."
                raise ApplicationError(msg)
            brand = brand_dict.get(item["brand_code"])
            mount = mount_dict.get(item["mount_code"])
            if not brand:
                msg = f"Brand with code '{item['brand_code']}' does not exist."
                raise ApplicationError(msg)
            if not mount:
                msg = f"Mount Type with code '{item['mount_code']}' does not exist."
                raise ApplicationError(msg)
            if stabilizer_check_mount_and_brand(
                brand=brand,
                mount=mount,
            ):
                msg = (
                    f"Stabilizer with brand '{brand.code}' and mount type "
                    f"'{mount.code}' already exists."
                )
                raise ApplicationError(msg)
            stabilizers.append(
                Stabilizer(
                    code=item["code"],
                    label=item["label"],
                    brand=brand,
                    mount=mount,
                    is_lubed=item["is_lubed"],
                    price=item["price"],
                    image=item["image"],
                    description=item["description"],
                ),
            )

        created = stabilizer_bulk_create(stabilizers=stabilizers)
        output = self.OutputSerializer(created, many=True)
        return Response(output.data, status=status.HTTP_201_CREATED)
