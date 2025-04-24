import hashlib
import hmac


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
