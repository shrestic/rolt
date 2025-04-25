import urllib.parse
from datetime import UTC
from datetime import datetime

from django.conf import settings
from django.db import transaction

from rolt.common.utils import get_object
from rolt.shop.models.order_model import Order
from rolt.shop.models.payment_transaction_model import PaymentTransaction
from rolt.shop.utils import generate_secure_hash
from rolt.shop.utils import generate_txn_ref
from rolt.shop.utils import get_client_ip
from rolt.shop.utils import parse_datetime_from_string
from rolt.shop.utils import verify_vnpay_signature


def payment_transaction_create(*, order: Order) -> PaymentTransaction:
    txn_ref = generate_txn_ref()
    return PaymentTransaction.objects.create(
        order=order,
        txn_ref=txn_ref,
        method=PaymentTransaction.MethodChoices.VNPAY,
        status=PaymentTransaction.StatusChoices.PENDING,
        amount=order.total_amount,
    )


def _generate_payment_transaction_err_msg(*, response_code: str):
    if response_code == "00":
        pass
    if response_code == "02":
        msg = "Order already confirmed"
        raise ValueError(msg)
    if response_code == "04":
        msg = "Invalid amount"
        raise ValueError(msg)
    if response_code == "01":
        msg = "Order not found"
        raise ValueError(msg)
    if response_code == "97":
        msg = "Invalid Checksum"
        raise ValueError(msg)


def payment_transaction_get_by_txn_ref(*, txn_ref: str) -> PaymentTransaction:
    return get_object(PaymentTransaction, txn_ref=txn_ref)


def payment_transaction_update(*, data: dict, payment_transaction: PaymentTransaction):
    if data["response_code"] == "00":
        with transaction.atomic():
            payment_transaction.status = PaymentTransaction.StatusChoices.SUCCESS
            payment_transaction.transaction_no = data["transaction_no"]
            payment_transaction.bank_code = data["bank_code"]
            payment_transaction.paid_at = parse_datetime_from_string(data["paid_at"])
            payment_transaction.message = data["message"]
            payment_transaction.save(
                update_fields=[
                    "status",
                    "transaction_no",
                    "bank_code",
                    "paid_at",
                    "message",
                ],
            )

            # Update order status to PAID
            order = payment_transaction.order
            order.status = Order.StatusChoices.PAID
            order.save(update_fields=["status"])
    else:
        payment_transaction.status = PaymentTransaction.StatusChoices.FAILED
        payment_transaction.message = data["message"]
        payment_transaction.save(update_fields=["status", "message"])
        _generate_payment_transaction_err_msg(response_code=data["response_code"])


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


def validate_and_extract_data(*, request):
    # Verify signature
    data = request.GET.dict()
    if not verify_vnpay_signature(data):
        msg = "Invalid signature"
        raise ValueError(msg)

    txn_ref = data.get("vnp_TxnRef")
    response_code = data.get("vnp_ResponseCode")
    transaction_status = data.get("vnp_TransactionStatus")
    transaction_no = data.get("vnp_TransactionNo")
    bank_code = data.get("vnp_BankCode")
    paid_at = data.get("vnp_PayDate")
    message = data.get("vnp_OrderInfo", "")

    # Validate required params
    if not all(
        [
            txn_ref,
            response_code,
            transaction_status,
            transaction_no,
            bank_code,
            paid_at,
            message,
        ],
    ):
        msg = "Missing required parameters"
        raise ValueError(msg)

    return {
        "txn_ref": txn_ref,
        "response_code": response_code,
        "transaction_status": transaction_status,
        "transaction_no": transaction_no,
        "bank_code": bank_code,
        "paid_at": paid_at,
        "message": message,
    }
