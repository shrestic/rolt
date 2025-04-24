from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.core.exceptions import ApplicationError
from rolt.shop.models.order_model import Order
from rolt.shop.selectors.order_selectors import order_get
from rolt.shop.services.payment_transaction_services import generate_payment_url
from rolt.shop.services.payment_transaction_services import payment_transaction_create


class PaymentCreateApi(APIView):
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
        if order.status != Order.StatusChoices.PENDING:
            msg = "Order is not pending"
            raise ApplicationError(msg)

        payment_transaction = payment_transaction_create(order=order)
        payment_url = generate_payment_url(
            order=order,
            payment_transaction=payment_transaction,
            request=request,
        )

        return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)
