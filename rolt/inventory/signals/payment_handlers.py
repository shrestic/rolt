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
    - Updates order to CANCELLED for failed/cancelled payments after success
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

    # Handle cancel/fail after success → update order to CANCELLED
    elif (
        payment_transaction.status
        in [
            PaymentTransaction.StatusChoices.FAILED,
            PaymentTransaction.StatusChoices.CANCELLED,
        ]
        and old_status == PaymentTransaction.StatusChoices.SUCCESS
    ):
        logger.info(
            "[PAYMENT RESTORE] Updating order %s status to CANCELLED",
            order.id,
        )

        with transaction.atomic():
            # Update order status - this will trigger inventory restoration via Order signals  # noqa: E501
            order.status = Order.StatusChoices.CANCELLED
            order.save(update_fields=["status"])

        logger.info("Order %s marked as CANCELLED", order.id)

    else:
        logger.debug(
            "Unhandled status transition: %s → %s. No order status change needed.",
            old_status,
            payment_transaction.status,
        )
