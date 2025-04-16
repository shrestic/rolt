from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.common.pagination import LimitOffsetPagination
from rolt.component_types.models import ComponentType
from rolt.component_types.services import component_type_check_label_and_applied_to
from rolt.component_types.services import component_type_create
from rolt.component_types.services import component_type_delete
from rolt.component_types.services import component_type_get
from rolt.component_types.services import component_type_list
from rolt.component_types.services import component_type_update
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsProductManager


class ComponentTypeCreateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ComponentType
            fields = [
                "code",
                "label",
                "applies_to",
                "note",
            ]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        existed_component_type = component_type_get(
            code=serializer.validated_data["code"],
        )
        if existed_component_type:
            msg = "ComponentType with this code already exists"
            raise ApplicationError(
                msg,
            )
        is_same_label_and_applied_to = component_type_check_label_and_applied_to(
            label=serializer.validated_data["label"],
            applies_to=serializer.validated_data["applies_to"],
        )
        if is_same_label_and_applied_to:
            msg = "ComponentType with this label and applies_to already exists"
            raise ApplicationError(
                msg,
            )
        component_type = component_type_create(**serializer.validated_data)
        return Response(component_type.code, status=status.HTTP_201_CREATED)


class ComponentTypeListApi(APIView):
    permission_classes = [AllowAny]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        label = serializers.CharField(required=False)
        applies_to = serializers.CharField(required=False)
        note = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ComponentType
            fields = [
                "code",
                "label",
                "applies_to",
            ]

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        component_types = component_type_list(
            filters=filters_serializer.validated_data,
        )
        serializer = self.OutputSerializer(component_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComponentTypeDetailApi(APIView):
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ComponentType
            fields = [
                "code",
                "label",
                "applies_to",
            ]

    def get(self, request, code):
        component_type = component_type_get(code=code)
        if not component_type:
            raise ApplicationError(
                message="ComponentType not found.",
            )
        serializer = self.OutputSerializer(component_type)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComponentTypeUpdateApi(APIView):
    permission_classes = [IsProductManager]

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ComponentType
            fields = [
                "label",
                "applies_to",
                "note",
            ]

    def patch(self, request, code):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        component_type = component_type_get(code=code)
        if not component_type:
            raise ApplicationError(
                message="ComponentType not found.",
            )
        component_type_update(instance=component_type, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ComponentTypeDeleteApi(APIView):
    permission_classes = [IsProductManager]

    def delete(self, request, code):
        component_type = component_type_get(code=code)
        if not component_type:
            raise ApplicationError(
                message="ComponentType not found.",
            )
        component_type_delete(instance=component_type)
        return Response(status=status.HTTP_204_NO_CONTENT)
