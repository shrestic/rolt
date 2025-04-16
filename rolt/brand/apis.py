from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.brand.models import Brand
from rolt.brand.services import brand_bulk_create
from rolt.brand.services import brand_create
from rolt.brand.services import brand_delete
from rolt.brand.services import brand_get
from rolt.brand.services import brand_list
from rolt.brand.services import brand_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class BrandCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = [
                "code",
                "label",
                "logo",
            ]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        existed_brand = brand_get(code=serializer.validated_data["code"])
        if existed_brand:
            msg = "Brand with this code already exists"
            raise ApplicationError(
                msg,
            )
        brand = brand_create(**serializer.validated_data)
        return Response(brand.code, status=status.HTTP_201_CREATED)


class BrandBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class BrandSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = [
                "code",
                "label",
                "logo",
            ]

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(
                message="Expected a list of brand.",
            )
        serializer = self.BrandSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for brand in serializer.validated_data:
            existed_brand = brand_get(code=brand["code"])
            if existed_brand:
                msg = "Brand with this code already exists"
                raise ApplicationError(msg)
        brands = brand_bulk_create(data=serializer.validated_data)
        serializer = self.BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = [
                "code",
                "label",
                "logo",
            ]

    def get(self, request):
        brands = brand_list()
        serializer = self.OutputSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = [
                "code",
                "label",
                "logo",
            ]

    def get(self, request, code):
        brand = brand_get(code=code)
        if not brand:
            raise ApplicationError(
                message="Brand not found.",
            )
        serializer = self.OutputSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Brand
            fields = [
                "label",
                "logo",
            ]

    def patch(self, request, code):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        brand = brand_get(code=code)
        if not brand:
            raise ApplicationError(
                message="Brand not found.",
            )
        brand_update(instance=brand, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class BrandDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        brand = brand_get(code=code)
        if not brand:
            raise ApplicationError(
                message="Brand not found.",
            )
        brand_delete(instance=brand)
        return Response(status=status.HTTP_204_NO_CONTENT)
