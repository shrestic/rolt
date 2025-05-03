from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from rolt.accounts.selectors.customer_selector import CustomerSelector
from rolt.core.exceptions import ApplicationError
from rolt.core.permissions import IsCustomer
from rolt.shop.models.order_model import Order
from rolt.shop.models.payment_transaction_model import PaymentTransaction
from rolt.shop.selectors.order_selectors import order_get
from rolt.shop.selectors.payment_transaction_selectors import payment_transaction_get
from rolt.shop.selectors.payment_transaction_selectors import (
    payment_transaction_get_by_txn_ref,
)
from rolt.shop.selectors.payment_transaction_selectors import (
    payment_transaction_list_by_customer,
)
from rolt.shop.services.payment_transaction_services import generate_payment_url
from rolt.shop.services.payment_transaction_services import payment_transaction_create
from rolt.shop.services.payment_transaction_services import payment_transaction_update
from rolt.shop.services.payment_transaction_services import validate_and_extract_data


class PaymentCreateApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payment_create"

    def get(self, request, order_id):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)
        order = order_get(id=order_id, customer=customer)
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


class PaymentReturnApi(APIView):
    def get(self, request):
        return Response(request.GET.dict(), status=status.HTTP_200_OK)


class PaymentIPNApi(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payment_update"

    def get(self, request):
        try:
            # Validate input and signature
            data = validate_and_extract_data(request=request)
            # Get payment transaction
            payment_transaction = payment_transaction_get_by_txn_ref(
                txn_ref=data["txn_ref"],
            )
            if not payment_transaction:
                msg = "Transaction not found"
                raise ApplicationError(msg)  # noqa: TRY301

            # Prevent re-processing
            if payment_transaction.status == payment_transaction.StatusChoices.SUCCESS:
                return Response(
                    "Transaction already confirmed",
                    status=status.HTTP_200_OK,
                )

            # Update transaction
            payment_transaction_update(
                data=data,
                payment_transaction=payment_transaction,
            )
            return Response("IPN handled successfully", status=status.HTTP_200_OK)

        except (ValueError, Exception) as e:
            raise ApplicationError(str(e))  # noqa: B904


class PaymentTransactionListApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payment_list"

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PaymentTransaction
            fields = [
                "id",
                "order",
                "txn_ref",
                "status",
                "amount",
                "bank_code",
                "transaction_no",
            ]

    def get(self, request):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)
        payment_transactions = payment_transaction_list_by_customer(customer=customer)
        if not payment_transactions:
            msg = "No payment transactions found"
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(payment_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentTransactionDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payment_detail"

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PaymentTransaction
            fields = [
                "id",
                "order",
                "txn_ref",
                "status",
                "amount",
                "bank_code",
                "transaction_no",
            ]

    def get(self, request, pk):
        customer = CustomerSelector().customer_get(user_id=request.user.id)
        if not customer:
            msg = "Customer not found"
            raise ApplicationError(msg)
        payment_transaction = payment_transaction_get(id=pk, customer=customer)
        if not payment_transaction:
            msg = "Payment transaction not found"
            raise ApplicationError(msg)
        serializer = self.OutputSerializer(payment_transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
