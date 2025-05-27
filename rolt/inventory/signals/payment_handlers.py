import logging

from django.db import transaction

from rolt.shop.models.order_model import Order
from rolt.shop.models.payment_transaction_model import PaymentTransaction

logger = logging.getLogger(__name__)


def process_payment_inventory_change(
    payment_transaction: PaymentTransaction,
    old_status: str,
):
    """
    Handle order status changes based on payment transaction status changes.
    Since inventory is already managed by Order signals, this function only
    updates the order status which will trigger the appropriate inventory changes.
    - Updates order to PAID for successful payments
    - Keeps order unchanged for failed/cancelled payments (no inventory restoration)
    """
    logger.info(
        "[PAYMENT PROCESSING] Payment %s - status=%s - old_status=%s",
        payment_transaction.txn_ref,
        payment_transaction.status,
        old_status,
    )

    if payment_transaction.status == old_status:
        logger.debug("No status change; skipping order status update.")
        return

    order = payment_transaction.order

    # Handle payment success → update order to PAID
    if (
        payment_transaction.status == PaymentTransaction.StatusChoices.SUCCESS
        and old_status != PaymentTransaction.StatusChoices.SUCCESS
    ):
        logger.info(
            "[PAYMENT SUCCESS] Updating order %s status to PAID",
            order.id,
        )
        with transaction.atomic():
            # Update order status - this will trigger inventory deduction via Order signals  # noqa: E501
            order.status = Order.StatusChoices.PAID
            order.save(update_fields=["status"])
        logger.info("Order %s marked as PAID", order.id)

    # Handle payment failures/cancellations → keep order unchanged
    elif payment_transaction.status in [
        PaymentTransaction.StatusChoices.FAILED,
        PaymentTransaction.StatusChoices.CANCELLED,
    ]:
        logger.info(
            "[PAYMENT FAILED/CANCELLED] Payment %s failed/cancelled - keeping order %s unchanged",  # noqa: E501
            payment_transaction.txn_ref,
            order.id,
        )
        # Order remains in its current state (likely PENDING)
        # Inventory remains checked but not deducted
        # No restoration needed since inventory was never deducted

    else:
        logger.debug(
            "Unhandled status transition: %s → %s. No order status change needed.",
            old_status,
            payment_transaction.status,
        )
