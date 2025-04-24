from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.core.exceptions import ApplicationError
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem
from rolt.shop.selectors.cart_selectors import cart_item_list
from rolt.shop.selectors.order_selectors import order_get
from rolt.shop.selectors.order_selectors import order_list_by_customer
from rolt.shop.services.order_services import order_create
from rolt.shop.services.order_services import order_update_status

OrderStatus = Order.StatusChoices


class OrderItemOutputSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_type",
            "object_id",
            "name_snapshot",
            "price_snapshot",
            "quantity",
        ]

    def get_product_type(self, obj):
        return obj.content_type.model


class OrderOutputSerializer(serializers.ModelSerializer):
    items = OrderItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]


class OrderCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)

        cart_items = cart_item_list(customer=customer)
        if not cart_items:
            msg = "Cart is empty"
            raise ApplicationError(msg)

        try:
            order = order_create(customer=customer, cart_items=cart_items)
        except ValueError as e:
            raise ApplicationError(str(e))  # noqa: B904

        serializer = OrderOutputSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)

        orders = order_list_by_customer(customer=customer)
        serializer = OrderOutputSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)

        order = order_get(id=pk, customer=customer)
        if not order:
            msg = "Order not found"
            raise ApplicationError(msg)

        serializer = OrderOutputSerializer(order)
        return Response(serializer.data)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)


class OrderStatusUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)

        order = order_get(id=pk, customer=customer)
        if not order:
            msg = "Order not found"
            raise ApplicationError(msg)
        order_update_status(
            order=order,
            status=serializer.validated_data["status"],
        )
        return Response({"message": "Order status updated."}, status=status.HTTP_200_OK)
