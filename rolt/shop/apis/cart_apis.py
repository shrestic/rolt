from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.shop.models.cart_model import CartItem
from rolt.shop.selectors.cart_selectors import cart_exist
from rolt.shop.selectors.cart_selectors import cart_item_list
from rolt.shop.services.cart_services import cart_clear
from rolt.shop.services.cart_services import cart_item_create_update
from rolt.shop.services.cart_services import cart_item_delete
from rolt.shop.services.cart_services import convert_to_product
from rolt.shop.utils import get_product_price


class OutputSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "added_at", "product_data"]

    def get_product_data(self, obj):
        product = obj.product
        if not product:
            return None

        return {
            "id": str(product.id),
            "name": getattr(product, "name", None),
            "price": get_product_price(product),
            "type": product.__class__.__name__.lower(),
        }


class CartItemCreateUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_create"

    class InputSerializer(serializers.Serializer):
        product_type = serializers.CharField()
        product_id = serializers.UUIDField()
        quantity = serializers.IntegerField(min_value=1)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_type = serializer.validated_data["product_type"]
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)

        try:
            product = convert_to_product(
                product_id=product_id,
                product_type=product_type,
            )
            cart_item = cart_item_create_update(
                customer=customer,
                product=product,
                quantity=quantity,
            )
        except ValueError as e:
            raise ApplicationError(str(e)) from e
        serializer = OutputSerializer(cart_item)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CartItemListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_list"

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        if not cart_exist(customer=customer):
            msg = "Cart does not exist."
            raise ApplicationError(msg)
        cart_items = cart_item_list(customer=customer)
        if not cart_items:
            msg = "Cart is empty."
            raise ApplicationError(msg)
        serializers = OutputSerializer(cart_items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CartItemDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_delete"

    def delete(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        deleted, _ = cart_item_delete(id=pk, customer=customer)
        if not deleted:
            msg = "Cart item not found."
            raise ApplicationError(msg)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "cart_delete"

    def post(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        cleared = cart_clear(customer=customer)
        if not cleared:
            msg = "Cart not found."
            raise ApplicationError(msg)
        return Response(status=status.HTTP_204_NO_CONTENT)
