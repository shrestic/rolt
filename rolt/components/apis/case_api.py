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
from rolt.components.models.case_model import Case
from rolt.components.selectors.case_selector import (
    case_check_material_and_mount_style_and_brand,
)
from rolt.components.selectors.case_selector import case_get
from rolt.components.selectors.case_selector import case_list
from rolt.components.services.case_service import case_bulk_create
from rolt.components.services.case_service import case_create
from rolt.components.services.case_service import case_delete
from rolt.components.services.case_service import case_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class CaseListApi(APIView):
    permission_classes = [AllowAny]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        label = serializers.CharField(required=False)
        brand = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        material = serializers.CharField(required=False)
        material_code = serializers.CharField(required=False)
        mount_style = serializers.CharField(required=False)
        mount_style_code = serializers.CharField(required=False)
        color = serializers.CharField(required=False)
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
        material = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )
        mount_style = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Case
            fields = [
                "code",
                "label",
                "brand",
                "material",
                "mount_style",
                "color",
                "price",
                "image",
                "description",
            ]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        cases = case_list(filters=filters_serializer.validated_data)
        serializer = self.OutputSerializer(cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CaseDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        brand = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "logo": serializers.ImageField(),
            },
        )
        material = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )
        mount_style = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Case
            fields = [
                "code",
                "label",
                "brand",
                "material",
                "mount_style",
                "color",
                "price",
                "image",
                "description",
            ]

    def get(self, request, code):
        case = case_get(code=code)
        if not case:
            msg = "Case with this code does not exist."
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(case)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CaseCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        material_code = serializers.CharField()
        mount_style_code = serializers.CharField()
        color = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        brand = brand_get(code=serializer.validated_data["brand_code"])
        material = component_type_get(code=serializer.validated_data["material_code"])
        mount_style = component_type_get(
            code=serializer.validated_data["mount_style_code"],
        )

        if not brand or not material or not mount_style:
            msg = "Brand, material or mount style is invalid."
            raise ApplicationError(msg)

        if case_get(code=serializer.validated_data["code"]):
            msg = "Case with this code already exists."
            raise ApplicationError(msg)

        if case_check_material_and_mount_style_and_brand(
            brand=brand,
            material=material,
            mount_style=mount_style,
        ):
            msg = "Case with this brand, material and mount style already exists."
            raise ApplicationError(msg)

        case = case_create(
            code=serializer.validated_data["code"],
            label=serializer.validated_data["label"],
            brand=brand,
            material=material,
            mount_style=mount_style,
            color=serializer.validated_data["color"],
            price=serializer.validated_data["price"],
            image=serializer.validated_data.get("image"),
            description=serializer.validated_data.get("description", ""),
        )
        return Response(case.code, status=status.HTTP_201_CREATED)


class CaseUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        brand_code = serializers.CharField(required=False)
        material_code = serializers.CharField(required=False)
        mount_style_code = serializers.CharField(required=False)

        class Meta:
            model = Case
            fields = [
                "label",
                "brand_code",
                "material_code",
                "mount_style_code",
                "color",
                "price",
                "image",
                "description",
            ]

    def patch(self, request, code):
        case = case_get(code=code)
        if not case:
            msg = "Case with this code does not exist."
            raise ApplicationError(msg)

        serializer = self.InputSerializer(case, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        brand = (
            brand_get(code=serializer.validated_data.pop("brand_code", None))
            if "brand_code" in serializer.validated_data
            else None
        )
        material = (
            component_type_get(
                code=serializer.validated_data.pop("material_code", None),
            )
            if "material_code" in serializer.validated_data
            else None
        )
        mount_style = (
            component_type_get(
                code=serializer.validated_data.pop("mount_style_code", None),
            )
            if "mount_style_code" in serializer.validated_data
            else None
        )

        if brand:
            serializer.validated_data["brand"] = brand
        if material:
            serializer.validated_data["material"] = material
        if mount_style:
            serializer.validated_data["mount_style"] = mount_style

        if brand and material and mount_style:
            if case_check_material_and_mount_style_and_brand(
                brand=brand,
                material=material,
                mount_style=mount_style,
            ):
                msg = "Case with this brand, material and mount style already exists."
                raise ApplicationError(msg)

        case = case_update(instance=case, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class CaseDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        case = case_get(code=code)
        if not case:
            msg = "Case with this code does not exist."
            raise ApplicationError(
                msg,
                extra={"code": code},
            )
        case_delete(instance=case)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CaseBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        material_code = serializers.CharField()
        mount_style_code = serializers.CharField()
        color = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Case
            fields = "__all__"

    def post(self, request):
        if not isinstance(request.data, list):
            msg = "Expected a list of cases."
            raise ApplicationError(msg)

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        brand_dict = brand_get_dict_by_codes([d["brand_code"] for d in data])
        material_dict = component_type_get_dict_by_codes(
            [d["material_code"] for d in data],
        )
        mount_dict = component_type_get_dict_by_codes(
            [d["mount_style_code"] for d in data],
        )

        cases = []
        for item in data:
            if case_get(code=item["code"]):
                msg = f"Case with code '{item['code']}' already exists."
                raise ApplicationError(msg)

            brand = brand_dict.get(item["brand_code"])
            material = material_dict.get(item["material_code"])
            mount = mount_dict.get(item["mount_style_code"])

            if not brand:
                msg = f"Brand with code '{item['brand_code']}' does not exist."
                raise ApplicationError(msg)
            if not material:
                msg = f"Material with code '{item['material_code']}' does not exist."
                raise ApplicationError(msg)
            if not mount:
                msg = f"Mount style with code '{item['mount_style_code']}' does not exist."  # noqa: E501
                raise ApplicationError(msg)

            if case_check_material_and_mount_style_and_brand(
                brand=brand,
                material=material,
                mount_style=mount,
            ):
                msg = (
                    f"Case with brand '{brand.code}', material '{material.code}', "
                    f"and mount style '{mount.code}' already exists."
                )
                raise ApplicationError(msg)

            cases.append(
                Case(
                    code=item["code"],
                    label=item["label"],
                    brand=brand,
                    material=material,
                    mount_style=mount,
                    color=item["color"],
                    price=item["price"],
                    image=item.get("image"),
                    description=item.get("description", ""),
                ),
            )

        created = case_bulk_create(cases=cases)
        output = self.OutputSerializer(created, many=True)
        return Response(output.data, status=status.HTTP_201_CREATED)
