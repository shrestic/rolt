import hashlib
import hmac
import secrets
import urllib
from datetime import UTC
from datetime import datetime

from django.conf import settings


def parse_datetime_from_string(value: str, fmt: str = "%Y%m%d%H%M%S") -> datetime:
    return datetime.strptime(value, fmt).replace(tzinfo=UTC)


def get_product_price(product):
    for field in ["price", "price_per_switch", "total_price"]:
        if hasattr(product, field):
            return getattr(product, field)
    return None


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


def generate_secure_hash(key: str, data: str) -> str:
    return hmac.new(
        key=key.encode("utf-8"),
        msg=data.encode("utf-8"),
        digestmod=hashlib.sha512,
    ).hexdigest()


def verify_vnpay_signature(data: dict) -> bool:
    received_hash = data.pop("vnp_SecureHash", "")
    sorted_response = sorted((k, v) for k, v in data.items() if k.startswith("vnp_"))
    encoded_params = [
        f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in sorted_response
    ]
    query_string = "&".join(encoded_params)
    expected_hash = generate_secure_hash(
        settings.VNPAY_HASH_SECRET_KEY,
        query_string,
    )

    return expected_hash == received_hash


def generate_txn_ref() -> str:
    return secrets.token_hex(10)
