from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.models.employee_model import Employee
from rolt.accounts.selectors.employee_selector import EmployeeSelector
from rolt.accounts.services.employee_service import EmployeeService
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsSupportOrProductManager
from rolt.users.serializers import UserSerializer


class MeEmployeeDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsSupportOrProductManager]

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Employee
            fields = [
                "phone",
                "address",
                "birth_date",
                "position",
                "department",
                "start_date",
                "user",
            ]

    def get(self, request):
        employee = EmployeeSelector().employee_get(user_id=request.user.id)

        if employee is None:
            raise ApplicationError(message="Employee not found")
        output_serializer = self.OutputSerializer(employee)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class MeEmployeeUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsSupportOrProductManager]

    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        birth_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        user = UserSerializer()

        class Meta:
            model = Employee
            fields = [
                "phone",
                "address",
                "birth_date",
                "position",
                "department",
                "start_date",
                "user",
            ]

    def patch(self, request):
        employee = EmployeeSelector().employee_get(user_id=request.user.id)
        if employee is None:
            raise ApplicationError(message="Employee not found")
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        employee = EmployeeService().employee_update(
            data=input_serializer.validated_data,
            employee=employee,
        )
        output_serializer = self.OutputSerializer(employee)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
