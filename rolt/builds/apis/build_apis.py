from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.builds.models import Build
from rolt.builds.selectors import build_check_duplicate_combo
from rolt.builds.selectors import build_exists
from rolt.builds.selectors import build_get_by_id
from rolt.builds.selectors import customer_build_get_by_id
from rolt.builds.selectors import customer_build_list
from rolt.builds.selectors import preset_build_get_by_id
from rolt.builds.selectors import preset_builds_list
from rolt.builds.services import build_create
from rolt.builds.services import build_delete
from rolt.builds.services import build_update
from rolt.common.utils import inline_serializer
from rolt.common.utils import user_in_group
from rolt.components.selectors.keycap_selectors import keycap_get
from rolt.components.selectors.kit_selectors import kit_get
from rolt.components.selectors.switch_selectors import switch_get
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.core.permissions import IsCustomerOrProductManager


class BuildOutputSerializer(serializers.ModelSerializer):
    kit = inline_serializer(
        fields={
            "code": serializers.CharField(),
            "name": serializers.CharField(),
        },
    )
    switch = inline_serializer(
        fields={
            "code": serializers.CharField(),
            "name": serializers.CharField(),
        },
    )
    keycap = inline_serializer(
        fields={
            "code": serializers.CharField(),
            "name": serializers.CharField(),
        },
    )

    class Meta:
        model = Build
        fields = [
            "id",
            "name",
            "kit",
            "switch",
            "switch_quantity",
            "keycap",
            "total_price",
            "created_at",
        ]


class CustomerBuildListApi(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        builds = customer_build_list(customer=customer)
        serializer = BuildOutputSerializer(builds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PresetBuildListApi(APIView):
    permission_classes = [AllowAny]  # Anyone can view

    def get(self, request):
        builds = preset_builds_list()
        serializer = BuildOutputSerializer(builds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerBuildDetailApi(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, build_id):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        build = customer_build_get_by_id(
            build_id=build_id,
            customer=customer,
        )
        if not build:
            msg = "Build not found or not owned by you"
            raise ApplicationError(msg)
        serializer = BuildOutputSerializer(build)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PresetBuildDetailApi(APIView):
    permission_classes = [AllowAny]

    def get(self, request, build_id):
        build = preset_build_get_by_id(build_id=build_id)
        if not build:
            msg = "Preset build not found"
            raise ApplicationError(msg)
        serializer = BuildOutputSerializer(build)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuildCreateApi(APIView):
    permission_classes = [IsCustomerOrProductManager]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        kit_code = serializers.CharField()
        switch_code = serializers.CharField()
        keycap_code = serializers.CharField()
        switch_quantity = serializers.IntegerField(min_value=1)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Lookup components
        kit = kit_get(code=data["kit_code"])
        switch = switch_get(code=data["switch_code"])
        keycap = keycap_get(code=data["keycap_code"])

        if not all([kit, switch, keycap]):
            raise ApplicationError(message="Kit, switch, or keycap not found")

        switch_quantity = data["switch_quantity"]
        name = data.get("name", "Build")

        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        # Customer build flow
        if is_customer:
            customer = CustomerSelector().customer_get(user_id=user.id)
            if customer is None:
                raise ApplicationError(message="Customer not found")

            if build_exists(
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=customer,
            ):
                raise ApplicationError(message="You already created this build")

            build = build_create(
                name=name,
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=customer,
                is_preset=False,
            )

        # Preset build flow
        elif is_product_manager:
            if build_exists(
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=None,
            ):
                raise ApplicationError(message="This preset build already exists")

            build = build_create(
                name=name,
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=None,
                is_preset=True,
            )

        else:
            raise ApplicationError(message="Permission denied")

        return Response({"id": build.id}, status=status.HTTP_201_CREATED)


class BuildUpdateApi(APIView):
    permission_classes = [IsCustomerOrProductManager]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        kit_code = serializers.CharField(required=False)
        switch_code = serializers.CharField(required=False)
        keycap_code = serializers.CharField(required=False)
        switch_quantity = serializers.IntegerField(min_value=1, required=False)

    def patch(self, request, pk):  # noqa: C901
        build = build_get_by_id(id=pk)
        if not build:
            raise ApplicationError(message="Build not found")

        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        # Determine build type and check ownership
        if build.customer:
            # Customer build
            if not is_customer or build.customer.user != user:
                raise ApplicationError(message="You can only update your own builds")
        else:  # noqa: PLR5501
            # Preset build
            if not is_product_manager:
                raise ApplicationError(
                    message="Only product managers can update preset builds",
                )

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        kit = switch = keycap = None

        if "kit_code" in data:
            kit = kit_get(code=data["kit_code"])
            if not kit:
                raise ApplicationError(message="Kit not found")

        if "switch_code" in data:
            switch = switch_get(code=data["switch_code"])
            if not switch:
                raise ApplicationError(message="Switch not found")

        if "keycap_code" in data:
            keycap = keycap_get(code=data["keycap_code"])
            if not keycap:
                raise ApplicationError(message="Keycap not found")

        # Check if the component combination already exists (excluding current build)
        is_duplicated = build_check_duplicate_combo(
            kit=kit,
            switch=switch,
            keycap=keycap,
            exclude_build_id=build.id,
            customer=build.customer,
        )
        if is_duplicated:
            raise ApplicationError(
                message="Another build already has this component combination.",
            )

        build = build_update(
            instance=build,
            name=data.get("name"),
            kit=kit,
            switch=switch,
            keycap=keycap,
            switch_quantity=data.get("switch_quantity"),
        )
        return Response(status=status.HTTP_200_OK)


class BuildDeleteApi(APIView):
    permission_classes = [IsCustomerOrProductManager]

    def delete(self, request, pk):
        build = build_get_by_id(id=pk)
        if not build:
            raise ApplicationError(message="Build not found")

        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        # If the build is a preset build (no customer)
        if build.customer is None:
            if not is_product_manager:
                raise ApplicationError(
                    message="Only product managers can delete preset builds",
                )
            build_delete(instance=build)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # If the build belongs to a customer
        if is_customer:
            if build.customer.user != user:
                raise ApplicationError(message="You can only delete your own builds")
            build_delete(instance=build)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Not authorized
        raise ApplicationError(
            message="You do not have permission to delete this build",
        )
