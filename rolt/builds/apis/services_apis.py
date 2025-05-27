from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rolt.builds.models import Service
from rolt.builds.selectors.service_selectors import service_get_by_code
from rolt.builds.selectors.service_selectors import service_list
from rolt.builds.services.service_services import service_create
from rolt.builds.services.service_services import service_delete
from rolt.builds.services.service_services import service_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class ServiceListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "service_list"  # 100/hour from LIST_RATE

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = [
                "id",
                "code",
                "name",
                "description",
                "price",
                "image",
            ]

    def get(self, request):
        services = service_list()
        serializer = self.OutputSerializer(services, many=True)
        return Response(serializer.data)


class ServiceCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "service_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(max_digits=14, decimal_places=0)
        image = serializers.ImageField(required=False, allow_null=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if service_get_by_code(code=data["code"]):
            msg = f"Service with code {data['code']} already exists"
            raise ApplicationError(msg)
        service_create(
            code=data["code"],
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            image=data.get("image", None),
        )
        return Response(status=status.HTTP_201_CREATED)


class ServiceUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "service_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(
            max_digits=14,
            decimal_places=0,
            required=False,
        )
        image = serializers.ImageField(required=False, allow_null=True)

    def patch(self, request, code):
        service = service_get_by_code(code=code)
        if not service:
            msg = "Service not found"
            raise ApplicationError(msg)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service_update(instance=service, data=data)
        return Response(status=status.HTTP_200_OK)


class ServiceDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsProductManager]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "service_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, code):
        service = service_get_by_code(code=code)
        if not service:
            msg = "Service not found"
            raise ApplicationError(msg)

        service_delete(instance=service)
        return Response(status=status.HTTP_204_NO_CONTENT)
