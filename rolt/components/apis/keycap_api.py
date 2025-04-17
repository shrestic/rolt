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
from rolt.components.models.keycap_model import Keycap
from rolt.components.selectors.keycap_selector import (
    keycap_check_material_and_profile_and_brand,
)
from rolt.components.selectors.keycap_selector import keycap_get
from rolt.components.selectors.keycap_selector import keycap_list
from rolt.components.services.keycap_service import keycap_bulk_create
from rolt.components.services.keycap_service import keycap_create
from rolt.components.services.keycap_service import keycap_delete
from rolt.components.services.keycap_service import keycap_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class KeycapListApi(APIView):
    permission_classes = [AllowAny]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        label = serializers.CharField(required=False)
        brand = serializers.CharField(required=False)
        brand_code = serializers.CharField(required=False)
        material = serializers.CharField(required=False)
        material_code = serializers.CharField(required=False)
        profile = serializers.CharField(required=False)
        profile_code = serializers.CharField(required=False)
        theme = serializers.CharField(required=False)
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
        profile = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Keycap
            fields = [
                "code",
                "label",
                "brand",
                "material",
                "profile",
                "theme",
                "price",
                "image",
                "description",
            ]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        keycaps = keycap_list(filters=filters_serializer.validated_data)
        serializer = self.OutputSerializer(keycaps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeycapDetailApi(APIView):
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
        profile = inline_serializer(
            fields={
                "code": serializers.CharField(),
                "label": serializers.CharField(),
                "applies_to": serializers.CharField(),
                "note": serializers.CharField(),
            },
        )

        class Meta:
            model = Keycap
            fields = [
                "code",
                "label",
                "brand",
                "material",
                "profile",
                "theme",
                "price",
                "image",
                "description",
            ]

    def get(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            msg = "Keycap with this code does not exist."
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(keycap)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeycapCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        material_code = serializers.CharField()
        profile_code = serializers.CharField()
        theme = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        brand = brand_get(code=serializer.validated_data["brand_code"])
        material = component_type_get(code=serializer.validated_data["material_code"])
        profile = component_type_get(code=serializer.validated_data["profile_code"])

        if not brand:
            msg = "Brand with this code does not exist."
            raise ApplicationError(msg)
        if not material:
            msg = "Material type does not exist."
            raise ApplicationError(msg)
        if not profile:
            msg = "Profile type does not exist."
            raise ApplicationError(msg)
        if keycap_get(code=serializer.validated_data["code"]):
            msg = "Keycap with this code already exists."
            raise ApplicationError(msg)
        if keycap_check_material_and_profile_and_brand(
            brand=brand,
            material=material,
            profile=profile,
        ):
            msg = "Keycap with this brand, material, and profile already exists."
            raise ApplicationError(msg)

        keycap = keycap_create(
            code=serializer.validated_data["code"],
            label=serializer.validated_data["label"],
            brand=brand,
            material=material,
            profile=profile,
            theme=serializer.validated_data["theme"],
            price=serializer.validated_data["price"],
            image=serializer.validated_data.get("image"),
            description=serializer.validated_data.get("description", ""),
        )
        return Response(keycap.code, status=status.HTTP_201_CREATED)


class KeycapUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        brand_code = serializers.CharField(required=False)
        material_code = serializers.CharField(required=False)
        profile_code = serializers.CharField(required=False)

        class Meta:
            model = Keycap
            fields = [
                "label",
                "brand_code",
                "material_code",
                "profile_code",
                "theme",
                "price",
                "image",
                "description",
            ]

    def patch(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            msg = "Keycap with this code does not exist."
            raise ApplicationError(msg)

        serializer = self.InputSerializer(keycap, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        brand_code = serializer.validated_data.pop("brand_code", None)
        material_code = serializer.validated_data.pop("material_code", None)
        profile_code = serializer.validated_data.pop("profile_code", None)

        brand = brand_get(code=brand_code) if brand_code else None
        material = component_type_get(code=material_code) if material_code else None
        profile = component_type_get(code=profile_code) if profile_code else None

        if brand:
            serializer.validated_data["brand"] = brand
        if material:
            serializer.validated_data["material"] = material
        if profile:
            serializer.validated_data["profile"] = profile

        if brand and material and profile:
            if keycap_check_material_and_profile_and_brand(
                brand=brand,
                material=material,
                profile=profile,
            ):
                msg = "Keycap with this brand, material, and profile already exists."
                raise ApplicationError(msg)

        keycap = keycap_update(instance=keycap, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class KeycapDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        keycap = keycap_get(code=code)
        if not keycap:
            msg = "Keycap with this code does not exist."
            raise ApplicationError(msg, extra={"code": code})
        keycap_delete(instance=keycap)
        return Response(status=status.HTTP_204_NO_CONTENT)


class KeycapBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        label = serializers.CharField()
        brand_code = serializers.CharField()
        material_code = serializers.CharField()
        profile_code = serializers.CharField()
        theme = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        image = serializers.ImageField(required=False, allow_null=True)
        description = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keycap
            fields = "__all__"

    def post(self, request):
        if not isinstance(request.data, list):
            msg = "Expected a list of keycaps."
            raise ApplicationError(msg)

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        brand_codes = [item["brand_code"] for item in data]
        material_codes = [item["material_code"] for item in data]
        profile_codes = [item["profile_code"] for item in data]

        brand_dict = brand_get_dict_by_codes(brand_codes)
        material_dict = component_type_get_dict_by_codes(material_codes)
        profile_dict = component_type_get_dict_by_codes(profile_codes)

        keycaps = []
        for item in data:
            if keycap_get(code=item["code"]):
                msg = f"Keycap with code '{item['code']}' already exists."
                raise ApplicationError(msg)

            brand = brand_dict.get(item["brand_code"])
            material = material_dict.get(item["material_code"])
            profile = profile_dict.get(item["profile_code"])

            if not brand:
                msg = f"Brand with code '{item['brand_code']}' does not exist."
                raise ApplicationError(msg)
            if not material:
                msg = (
                    f"Material type with code '{item['material_code']}' does not exist."
                )
                raise ApplicationError(msg)
            if not profile:
                msg = f"Profile type with code '{item['profile_code']}' does not exist."
                raise ApplicationError(msg)

            if keycap_check_material_and_profile_and_brand(
                brand=brand,
                material=material,
                profile=profile,
            ):
                msg = (
                    f"Keycap with brand '{brand.code}', material '{material.code}', "
                    f"and profile '{profile.code}' already exists."
                )
                raise ApplicationError(msg)

            keycaps.append(
                Keycap(
                    code=item["code"],
                    label=item["label"],
                    brand=brand,
                    material=material,
                    profile=profile,
                    theme=item["theme"],
                    price=item["price"],
                    image=item.get("image"),
                    description=item.get("description"),
                ),
            )

        created = keycap_bulk_create(keycaps=keycaps)
        output = self.OutputSerializer(created, many=True)
        return Response(output.data, status=status.HTTP_201_CREATED)
