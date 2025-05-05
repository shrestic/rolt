import logging
from datetime import timedelta

from django.utils import timezone

from rolt.accounts.models.customer_model import Customer
from rolt.shop.models.order_model import Order
from rolt.warranty.models import Warranty
from rolt.warranty.models import WarrantyRequest

logger = logging.getLogger(__name__)

# ----------Warranty Services----------#
WARRANTY_DURATION_MAP = {
    "kit": 365,  # 12 months
    "switch": 180,  # 6 months
    "keycap": 90,  # 3 months
    "build": 180,  # custom builds
    "accessory": 90,  # 3 months
}


def warranty_create(*, order: Order):
    orderitems = order.items.filter(warranty__isnull=True)
    if not orderitems.exists():
        logger.info(
            "Order already has all warranties created.",
            extra={"order_id": order.id},
        )
        return

    for orderitem in orderitems:
        model_key = orderitem.content_type.model.lower()
        duration_days = WARRANTY_DURATION_MAP.get(model_key, 90)  # fallback: 3 months
        start_date = timezone.now()
        end_date = start_date + timedelta(days=duration_days)
        Warranty.objects.create(
            orderitem=orderitem,
            customer=order.customer,
            start_date=start_date,
            end_date=end_date,
            status=Warranty.Status.ACTIVE,
            notes=f"Auto-created for product type '{model_key}' ({duration_days} days)",
        )


def warranty_void(*, instance: Warranty, note: str = "") -> Warranty:
    instance.status = Warranty.Status.VOIDED
    if note:
        instance.notes = note
    instance.save(update_fields=["status", "notes"])
    return instance


def warranty_mark_expired(*, instance: Warranty) -> Warranty:
    instance.status = Warranty.Status.EXPIRED
    instance.save(update_fields=["status"])
    return instance


def warranty_delete(*, instance: Warranty) -> None:
    instance.delete()


# ----------WarrantyRequest Services----------#
def warranty_request_create(
    *,
    warranty: Warranty,
    customer: Customer,
    description: str,
) -> WarrantyRequest:
    return WarrantyRequest.objects.create(
        warranty=warranty,
        customer=customer,
        description=description,
    )


def warranty_request_approve(
    *,
    instance: WarrantyRequest,
    note: str = "",
) -> WarrantyRequest:
    instance.status = WarrantyRequest.Status.APPROVED
    instance.admin_notes = note
    instance.save(update_fields=["status", "admin_notes"])
    return instance


def warranty_request_reject(
    *,
    instance: WarrantyRequest,
    note: str = "",
) -> WarrantyRequest:
    instance.status = WarrantyRequest.Status.REJECTED
    instance.admin_notes = note
    instance.save(update_fields=["status", "admin_notes"])
    return instance
