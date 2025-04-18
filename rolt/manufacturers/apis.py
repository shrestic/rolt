from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager
from rolt.manufacturers.models import Manufacturer
from rolt.manufacturers.services import manufacturer_bulk_create
from rolt.manufacturers.services import manufacturer_create
from rolt.manufacturers.services import manufacturer_delete
from rolt.manufacturers.services import manufacturer_get
from rolt.manufacturers.services import manufacturer_list
from rolt.manufacturers.services import manufacturer_update


class ManufacturerCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Manufacturer
            fields = [
                "code",
                "label",
                "logo",
            ]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        existed_manufacturer = manufacturer_get(code=serializer.validated_data["code"])
        if existed_manufacturer:
            msg = "manufacturer with this code already exists"
            raise ApplicationError(
                msg,
            )
        manufacturer = manufacturer_create(**serializer.validated_data)
        return Response(manufacturer.code, status=status.HTTP_201_CREATED)


class ManufacturerBulkCreateApi(APIView):
    permission_classes = [IsProductManager]

    class ManufacturerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Manufacturer
            fields = [
                "code",
                "label",
                "logo",
            ]

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(
                message="Expected a list of manufacturer.",
            )
        serializer = self.ManufacturerSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for item in serializer.validated_data:
            existed_manufacturer = manufacturer_get(code=item["code"])
            if existed_manufacturer:
                msg = "manufacturer with this code already exists"
                raise ApplicationError(msg)
        manufacturers = manufacturer_bulk_create(data=serializer.validated_data)
        serializer = self.ManufacturerSerializer(manufacturers, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ManufacturerListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Manufacturer
            fields = [
                "code",
                "label",
                "logo",
            ]

    def get(self, request):
        manufacturers = manufacturer_list()
        serializer = self.OutputSerializer(manufacturers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManufacturerDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Manufacturer
            fields = [
                "code",
                "label",
                "logo",
            ]

    def get(self, request, code):
        manufacturer = manufacturer_get(code=code)
        if not manufacturer:
            raise ApplicationError(
                message="manufacturer not found.",
            )
        serializer = self.OutputSerializer(manufacturer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManufacturerUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Manufacturer
            fields = [
                "label",
                "logo",
            ]

    def patch(self, request, code):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        manufacturer = manufacturer_get(code=code)
        if not manufacturer:
            raise ApplicationError(
                message="manufacturer not found.",
            )
        manufacturer_update(instance=manufacturer, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ManufacturerDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        manufacturer = manufacturer_get(code=code)
        if not manufacturer:
            raise ApplicationError(
                message="Manufacturer not found.",
            )
        manufacturer_delete(instance=manufacturer)
        return Response(status=status.HTTP_204_NO_CONTENT)
