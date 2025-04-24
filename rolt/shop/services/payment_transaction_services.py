import secrets
import urllib.parse
from datetime import UTC
from datetime import datetime
from datetime import timezone

from django.conf import settings
from django.db import transaction

from rolt.common.utils import get_object
from rolt.shop.models.order_model import Order
from rolt.shop.models.payment_transaction_model import PaymentTransaction
from rolt.shop.utils import generate_secure_hash
from rolt.shop.utils import get_client_ip


def generate_txn_ref() -> str:
    return secrets.token_hex(10)


def payment_transaction_create(*, order: Order) -> PaymentTransaction:
    txn_ref = generate_txn_ref()
    return PaymentTransaction.objects.create(
        order=order,
        txn_ref=txn_ref,
        method=PaymentTransaction.MethodChoices.VNPAY,
        status=PaymentTransaction.StatusChoices.PENDING,
        amount=order.total_amount,
    )


def payment_get_transaction_by_ref(*, txn_ref: str) -> PaymentTransaction:
    return get_object(PaymentTransaction, txn_ref=txn_ref)


def payment_mark_success(
    *,
    payment_transaction: PaymentTransaction,
    vnp_txn_no: str,
    bank_code: str,
    response_code: str,
) -> None:
    with transaction.atomic():
        payment_transaction.status = PaymentTransaction.StatusChoices.SUCCESS
        payment_transaction.response_code = response_code
        payment_transaction.vnp_txn_no = vnp_txn_no
        payment_transaction.bank_code = bank_code
        payment_transaction.paid_at = timezone.now()
        payment_transaction.save(
            update_fields=[
                "status",
                "response_code",
                "vnp_txn_no",
                "bank_code",
                "paid_at",
            ],
        )

        # Update order status to PAID
        order = payment_transaction.order
        order.status = Order.StatusChoices.PAID
        order.save(update_fields=["status"])


def payment_mark_failed(
    *,
    transaction: PaymentTransaction,
    response_code: str,
    message: str = "Failed or cancelled",
) -> None:
    transaction.status = PaymentTransaction.StatusChoices.FAILED
    transaction.response_code = response_code
    transaction.message = message
    transaction.save(update_fields=["status", "response_code", "message"])


def generate_payment_url(
    *,
    order: Order,
    payment_transaction: PaymentTransaction,
    request,
) -> str:
    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": settings.VNPAY_TMN_CODE,
        "vnp_Amount": str(int(order.total_amount * 100)),  # VNPAY uses VND * 100
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": payment_transaction.txn_ref,
        "vnp_OrderInfo": f"Payment for order {order.id}",
        "vnp_OrderType": "billpayment",
        "vnp_Locale": "vn",
        "vnp_IpAddr": get_client_ip(request),
        "vnp_CreateDate": datetime.now(UTC).strftime("%Y%m%d%H%M%S"),
        "vnp_ReturnUrl": settings.VNPAY_RETURN_URL,
    }

    sorted_params = sorted(params.items())
    encoded_params = [
        f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in sorted_params
    ]
    query_string = "&".join(encoded_params)

    secure_hash = generate_secure_hash(settings.VNPAY_HASH_SECRET_KEY, query_string)
    payment_url = (
        f"{settings.VNPAY_PAYMENT_URL}?{query_string}&vnp_SecureHash={secure_hash}"
    )
    return payment_url  # noqa: RET504
