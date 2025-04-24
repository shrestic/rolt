from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.builds.models import Build
from rolt.builds.selectors.build_selectors import build_check_duplicate_combo
from rolt.builds.selectors.build_selectors import build_exists
from rolt.builds.selectors.build_selectors import build_get_by_id
from rolt.builds.selectors.build_selectors import customer_build_get_by_id
from rolt.builds.selectors.build_selectors import customer_build_list
from rolt.builds.selectors.build_selectors import preset_build_get_by_id
from rolt.builds.selectors.build_selectors import preset_builds_list
from rolt.builds.selectors.service_selectors import service_list_by_codes
from rolt.builds.services.build_services import build_create
from rolt.builds.services.build_services import build_delete
from rolt.builds.services.build_services import build_update
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
        fields={"code": serializers.CharField(), "name": serializers.CharField()},
    )
    switch = inline_serializer(
        fields={"code": serializers.CharField(), "name": serializers.CharField()},
    )
    keycap = inline_serializer(
        fields={"code": serializers.CharField(), "name": serializers.CharField()},
    )
    selected_services = inline_serializer(
        many=True,
        fields={
            "service": inline_serializer(
                fields={
                    "code": serializers.CharField(),
                    "name": serializers.CharField(),
                },
            ),
            "price": serializers.DecimalField(max_digits=10, decimal_places=2),
        },
        source="selected_services.all",
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
            "selected_services",
            "created_at",
        ]


class CustomerBuildListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "build_list"  # 100/hour from LIST_RATE

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        builds = customer_build_list(customer=customer)
        serializer = BuildOutputSerializer(builds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PresetBuildListApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "build_list"  # 100/hour from LIST_RATE

    def get(self, request):
        builds = preset_builds_list()
        serializer = BuildOutputSerializer(builds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerBuildDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "build_detail"  # 200/hour from DETAIL_RATE

    def get(self, request, build_id):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if customer is None:
            raise ApplicationError(message="Customer not found")
        build = customer_build_get_by_id(id=build_id, customer=customer)
        if not build:
            msg = "Build not found or not owned by you"
            raise ApplicationError(msg)
        serializer = BuildOutputSerializer(build)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PresetBuildDetailApi(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "build_detail"  # 200/hour from DETAIL_RATE

    def get(self, request, build_id):
        build = preset_build_get_by_id(id=build_id)
        if not build:
            msg = "Preset build not found"
            raise ApplicationError(msg)
        serializer = BuildOutputSerializer(build)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuildCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "build_create"  # 100/hour from CREATE_RATE

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        kit_code = serializers.CharField()
        switch_code = serializers.CharField()
        keycap_code = serializers.CharField()
        switch_quantity = serializers.IntegerField(min_value=1)
        service_codes = serializers.ListField(
            child=serializers.CharField(),
            required=False,
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        kit = kit_get(code=data["kit_code"])
        switch = switch_get(code=data["switch_code"])
        keycap = keycap_get(code=data["keycap_code"])

        if not all([kit, switch, keycap]):
            msg = "Kit, switch, or keycap not found"
            raise ApplicationError(msg)

        switch_quantity = data["switch_quantity"]
        name = data.get("name", "Build")
        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        if is_customer:
            customer = CustomerSelector().customer_get(user_id=user.id)
            if customer is None:
                msg = "Customer not found"
                raise ApplicationError(msg)
            if build_exists(
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=customer,
            ):
                msg = "You already created this build"
                raise ApplicationError(msg)

            selected_services = service_list_by_codes(
                codes=data.get("service_codes", []),
            )
            build = build_create(
                name=name,
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=customer,
                is_preset=False,
                selected_services=selected_services,
            )

        elif is_product_manager:
            if build_exists(
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=None,
            ):
                msg = "This preset build already exists"
                raise ApplicationError(msg)

            build = build_create(
                name=name,
                kit=kit,
                switch=switch,
                keycap=keycap,
                switch_quantity=switch_quantity,
                customer=None,
                is_preset=True,
                selected_services=None,
            )
        else:
            msg = "Permission denied"
            raise ApplicationError(msg)

        return Response({"id": build.id}, status=status.HTTP_201_CREATED)


class BuildUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "build_update"  # 100/hour from UPDATE_RATE

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        kit_code = serializers.CharField(required=False)
        switch_code = serializers.CharField(required=False)
        keycap_code = serializers.CharField(required=False)
        switch_quantity = serializers.IntegerField(min_value=1, required=False)
        service_codes = serializers.ListField(
            child=serializers.CharField(),
            required=False,
        )

    def patch(self, request, pk):  # noqa: C901
        build = build_get_by_id(id=pk)
        if not build:
            msg = "Build not found"
            raise ApplicationError(msg)

        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        if build.customer:
            if not is_customer or build.customer.user != user:
                msg = "You can only update your own builds"
                raise ApplicationError(msg)
        elif not is_product_manager:
            msg = "Only product managers can update preset builds"
            raise ApplicationError(msg)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        kit = switch = keycap = None
        if "kit_code" in data:
            kit = kit_get(code=data["kit_code"])
            if not kit:
                msg = "Kit not found"
                raise ApplicationError(msg)
        if "switch_code" in data:
            switch = switch_get(code=data["switch_code"])
            if not switch:
                msg = "Switch not found"
                raise ApplicationError(msg)
        if "keycap_code" in data:
            keycap = keycap_get(code=data["keycap_code"])
            if not keycap:
                msg = "Keycap not found"
                raise ApplicationError(msg)

        is_duplicated = build_check_duplicate_combo(
            kit=kit or build.kit,
            switch=switch or build.switch,
            keycap=keycap or build.keycap,
            exclude_build_id=build.id,
            customer=build.customer,
        )
        if is_duplicated:
            msg = "Another build already has this component combination."
            raise ApplicationError(
                msg,
            )

        selected_services = None
        if not build.is_preset and "service_codes" in data:
            selected_services = service_list_by_codes(codes=data["service_codes"])

        build = build_update(
            instance=build,
            name=data.get("name"),
            kit=kit,
            switch=switch,
            keycap=keycap,
            switch_quantity=data.get("switch_quantity"),
            selected_services=selected_services,
        )
        return Response(status=status.HTTP_200_OK)


class BuildDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrProductManager]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "build_delete"  # 50/hour from DELETE_RATE

    def delete(self, request, pk):
        build = build_get_by_id(id=pk)
        if not build:
            msg = "Build not found"
            raise ApplicationError(msg)

        user = request.user
        is_customer = user_in_group(user, "Customer")
        is_product_manager = user_in_group(user, "Product Manager")

        if build.customer is None:
            if not is_product_manager:
                msg = "Only product managers can delete preset builds"
                raise ApplicationError(msg)
            build_delete(instance=build)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if is_customer:
            if build.customer.user != user:
                msg = "You can only delete your own builds"
                raise ApplicationError(msg)
            build_delete(instance=build)
            return Response(status=status.HTTP_204_NO_CONTENT)

        msg = "You do not have permission to delete this build"
        raise ApplicationError(msg)
