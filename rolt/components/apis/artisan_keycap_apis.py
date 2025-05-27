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
from rolt.components.models.artisan_keycap_model import ArtisanKeycap
from rolt.components.selectors.artisan_keycap_selectors import artisan_keycap_get
from rolt.components.selectors.artisan_keycap_selectors import (
    artisan_keycap_get_existing_codes,
)
from rolt.components.selectors.artisan_keycap_selectors import artisan_keycap_list
from rolt.components.services.artisan_keycap_services import ArtisanKeycapData
from rolt.components.services.artisan_keycap_services import artisan_keycap_bulk_create
from rolt.components.services.artisan_keycap_services import artisan_keycap_create
from rolt.components.services.artisan_keycap_services import artisan_keycap_delete
from rolt.components.services.artisan_keycap_services import artisan_keycap_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class ArtisanKeycapListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "keycap_list"

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArtisanKeycap
            fields = "__all__"

    def get(self, request):
        keycaps = artisan_keycap_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=keycaps,
            request=request,
            view=self,
        )


class ArtisanKeycapDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "keycap_detail"

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArtisanKeycap
            fields = "__all__"

    def get(self, request, code):
        keycap = artisan_keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Artisan keycap not found")
        serializer = self.OutputSerializer(keycap)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtisanKeycapCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_create"

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArtisanKeycap
            fields = "__all__"

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get("code")
        if artisan_keycap_get(code=code):
            raise ApplicationError(
                message=f"ArtisanKeycap with code '{code}' already exists",
            )
        keycap_data = ArtisanKeycapData(**serializer.validated_data)
        keycap = artisan_keycap_create(data=keycap_data)
        return Response({"code": keycap.code}, status=status.HTTP_201_CREATED)


class ArtisanKeycapUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_update"

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArtisanKeycap
            fields = "__all__"

    def patch(self, request, code):
        keycap = artisan_keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Artisan keycap not found")

        serializer = self.InputSerializer(keycap, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        keycap = artisan_keycap_update(instance=keycap, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ArtisanKeycapDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_delete"

    def delete(self, request, code):
        keycap = artisan_keycap_get(code=code)
        if not keycap:
            raise ApplicationError(message="Artisan keycap not found")
        artisan_keycap_delete(instance=keycap)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtisanKeycapBulkCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "keycap_bulk_create"

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ArtisanKeycap
            fields = "__all__"

    def post(self, request):
        if not isinstance(request.data, list):
            raise ApplicationError(message="Expected a list of artisan keycaps")

        serializer = self.InputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        codes = [item["code"] for item in serializer.validated_data]
        existing_codes = artisan_keycap_get_existing_codes(codes=codes)
        if existing_codes:
            msg = f"ArtisanKeycap(s) with code(s) {', '.join(existing_codes)} already exist."  # noqa: E501
            raise ApplicationError(message=msg)

        keycaps = [ArtisanKeycap(**item) for item in serializer.validated_data]
        created_keycaps = artisan_keycap_bulk_create(artisan_keycaps=keycaps)
        return Response(
            [keycap.code for keycap in created_keycaps],
            status=status.HTTP_201_CREATED,
        )
