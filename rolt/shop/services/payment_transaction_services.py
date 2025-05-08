import urllib.parse
from datetime import UTC
from datetime import datetime

from django.conf import settings
from django.db import transaction

from rolt.inventory.signals.payment_handlers import process_payment_inventory_change
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
    errors = {
        "01": "Order not found",
        "02": "Order already confirmed",
        "04": "Invalid amount",
        "07": "Suspicious transaction. Possibly related to fraud.",
        "09": "Transaction failed: Card/account not registered for Internet Banking.",
        "10": "Transaction failed: Authentication failed more than 3 times.",
        "11": "Transaction failed: Payment timeout. Please try again.",
        "12": "Transaction failed: Card/account is locked.",
        "13": "Transaction failed: Incorrect OTP. Please try again.",
        "24": "Transaction failed: Cancelled by customer.",
        "51": "Transaction failed: Insufficient funds.",
        "65": "Transaction failed: Exceeded daily transaction limit.",
        "75": "Transaction failed: Bank is under maintenance.",
        "79": "Transaction failed: Exceeded allowed PIN attempts. Please try again.",
        "97": "Invalid Checksum",
        "99": "Transaction failed: Unknown error.",
    }

    return errors.get(
        response_code,
        f"Transaction failed: Unrecognized error code {response_code}.",
    )


def payment_transaction_update(*, data: dict, payment_transaction: PaymentTransaction):
    old_status = payment_transaction.status

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
            process_payment_inventory_change(
                payment_transaction=payment_transaction,
                old_status=old_status,
            )
            order = payment_transaction.order
            order.status = Order.StatusChoices.PAID
            order.save(update_fields=["status"])
    else:
        error_msg = _generate_payment_transaction_err_msg(
            response_code=data["response_code"],
        )

        with transaction.atomic():
            payment_transaction.message = error_msg
            payment_transaction.status = PaymentTransaction.StatusChoices.FAILED
            payment_transaction.save(update_fields=["status", "message"])
            process_payment_inventory_change(
                payment_transaction=payment_transaction,
                old_status=old_status,
            )

        raise ValueError(error_msg)


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
