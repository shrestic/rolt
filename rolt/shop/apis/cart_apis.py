from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.shop.models.cart_model import Cart
from rolt.shop.selectors.cart_selectors import cart_exist
from rolt.shop.selectors.cart_selectors import cart_get
from rolt.shop.services.cart_services import cart_clear
from rolt.shop.services.cart_services import cart_create_update
from rolt.shop.services.cart_services import cart_delete
from rolt.shop.services.cart_services import convert_to_product


class OutputSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "quantity", "added_at", "product_data"]

    def _get_product_price(self, product):
        for field in ["price", "price_per_switch", "total_price"]:
            if hasattr(product, field):
                return getattr(product, field)
        return None

    def get_product_data(self, obj):
        product = obj.product
        if not product:
            return None

        return {
            "id": str(product.id),
            "name": getattr(product, "name", None),
            "price": self._get_product_price(product),
            "type": product.__class__.__name__.lower(),
        }


class CartCreateUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

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
            cart = cart_create_update(
                customer=customer,
                product=product,
                quantity=quantity,
            )
        except ValueError as e:
            raise ApplicationError(str(e)) from e
        serializer = OutputSerializer(cart)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CartDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        if not cart_exist(customer=customer):
            msg = "Cart does not exist."
            raise ApplicationError(msg)
        cart = cart_get(customer=customer)
        if not cart:
            msg = "Cart is empty."
            raise ApplicationError(msg)
        return Response(OutputSerializer(cart, many=True).data)


class CartDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        deleted, _ = cart_delete(pk, customer)
        if not deleted:
            msg = "Cart item not found."
            raise ApplicationError(msg)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found."
            raise ApplicationError(msg)
        cleared = cart_clear(customer)
        if not cleared:
            msg = "Cart not found."
            raise ApplicationError(msg)
        return Response(status=status.HTTP_204_NO_CONTENT)
