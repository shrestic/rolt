from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.builds.models import Service
from rolt.builds.selectors.service_selectors import service_get_by_code
from rolt.builds.selectors.service_selectors import service_list
from rolt.builds.services.service_services import service_create
from rolt.builds.services.service_services import service_delete
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class ServiceListApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Service
            fields = [
                "id",
                "code",
                "name",
                "description",
                "price",
            ]

    def get(self, request):
        services = service_list()
        serializer = self.OutputSerializer(services, many=True)
        return Response(serializer.data)


class ServiceCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(max_digits=10, decimal_places=2)

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
        )
        return Response(status=status.HTTP_201_CREATED)


class ServiceDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        service = service_get_by_code(code=code)
        if not service:
            msg = "Service not found"
            raise ApplicationError(msg)

        service_delete(instance=service)
        return Response(status=status.HTTP_204_NO_CONTENT)
