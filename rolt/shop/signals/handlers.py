import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import localtime

from rolt.email.models import Email
from rolt.email.services import email_send
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem
from rolt.shop.models.payment_transaction_model import PaymentTransaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def send_order_notification_email(instance, **_):
    """Send notification email based on the order status."""
    order: Order = instance
    try:
        # Define templates and subjects for each order status
        template_map = {
            Order.StatusChoices.PENDING: {
                "subject": f"[Rolt] Order Confirmation - {order.id}",
                "template": "email/pending_order_notify.html",
                "plain_text": (
                    f"Hello {order.customer.full_name},\n\n"
                    f"Thank you for your order!\n"
                    f"Order ID: {order.id}\n"
                    f"Status: {order.get_status_display()}\n"
                    f"Total: ${order.total_amount}\n"
                    f"Placed at: {localtime(order.created_at).strftime('%Y-%m-%d %H:%M')}\n\n"  # noqa: E501
                ),
            },
            Order.StatusChoices.PAID: {
                "subject": f"[Rolt] Payment Confirmation - {order.id}",
                "template": "email/paid_order_notify.html",
                "plain_text": (
                    f"Hello {order.customer.full_name},\n\n"
                    f"Your payment has been confirmed!\n"
                    f"Order ID: {order.id}\n"
                    f"Status: {order.get_status_display()}\n"
                    f"Total: ${order.total_amount}\n"
                    f"Placed at: {localtime(order.created_at).strftime('%Y-%m-%d %H:%M')}\n\n"  # noqa: E501
                ),
            },
            Order.StatusChoices.CANCELLED: {
                "subject": f"[Rolt] Order Cancelled - {order.id}",
                "template": "email/cancelled_order_notify.html",
                "plain_text": (
                    f"Hello {order.customer.full_name},\n\n"
                    f"We're sorry, your order has been cancelled.\n"
                    f"Order ID: {order.id}\n"
                    f"Status: {order.get_status_display()}\n"
                    f"Total: ${order.total_amount}\n"
                    f"Reason: Contact support for details.\n\n"
                ),
            },
            Order.StatusChoices.REFUNDED: {
                "subject": f"[Rolt] Refund Confirmation - {order.id}",
                "template": "email/refunded_order_notify.html",
                "plain_text": (
                    f"Hello {order.customer.full_name},\n\n"
                    f"Your refund has been processed.\n"
                    f"Order ID: {order.id}\n"
                    f"Status: {order.get_status_display()}\n"
                    f"Refund Amount: ${order.total_amount}\n"
                    f"Processed at: {localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')}\n\n"  # noqa: E501
                ),
            },
        }

        # Skip if the order status is not defined in the template map
        if order.status not in template_map:
            logger.debug(
                "Skipping email for order %s with unsupported status %s",
                order.id,
                order.status,
                extra={"order_id": order.id, "status": order.status},
            )
            return

        # Avoid sending email for PENDING orders if total_amount is not set
        if order.status == Order.StatusChoices.PENDING and order.total_amount == 0:
            logger.debug(
                "Skipping email for PENDING order %s as total_amount is not set",
                order.id,
                extra={"order_id": order.id},
            )
            return

        # Fetch OrderItem list with optimized queries
        items = OrderItem.objects.select_related("content_type").filter(order=order)
        config = template_map[order.status]
        context = {
            "customer_name": order.customer.full_name,
            "order_id": order.id,
            "status": order.get_status_display(),
            "total_amount": order.total_amount,
            "created_at": localtime(order.created_at).strftime("%Y-%m-%d %H:%M"),
            "items": items,
            "current_year": timezone.now().year,
        }

        # Render HTML template
        html = render_to_string(config["template"], context)

        # Create and send email
        email = Email.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=order.customer.user.email,
            subject=config["subject"],
            plain_text=config["plain_text"],
            html=html,
            status=Email.Status.SENDING,
        )
        email_send(email)
        logger.info(
            "Email sent for order %s with status %s",
            order.id,
            order.status,
            extra={"order_id": order.id, "status": order.status},
        )
    except Exception as e:
        logger.exception(
            "[ERROR] Order email notification failed",
            extra={"error": str(e), "order_id": order.id, "status": order.status},
        )


@receiver(post_save, sender=PaymentTransaction)
def send_payment_notification_email(sender, instance, created, **kwargs):
    transaction: PaymentTransaction = instance

    try:
        template_map = {
            PaymentTransaction.StatusChoices.FAILED: {
                "subject": f"[Rolt] Payment Failed - Order {transaction.order.id}",
                "template": "email/failed_payment_notify.html",
                "plain_text": (
                    f"Hello {transaction.order.customer.full_name},\n\n"
                    f"Your payment attempt for Order {transaction.order.id} has failed.\n"  # noqa: E501
                    f"Amount: ${transaction.amount}\n"
                    f"Reason: {transaction.message or 'Unknown error'}\n\n"
                ),
            },
        }

        # Skip if status is not in template_map (e.g., PENDING, CANCELLED)
        if transaction.status not in template_map:
            logger.debug(
                "Skipping email for payment transaction with unsupported status",
                extra={
                    "txn_ref": transaction.txn_ref,
                    "status": transaction.status,
                },
            )
            return

        # Skip if no associated order exists
        if not transaction.order:
            logger.debug(
                "Skipping email for payment transaction with no associated order",
                extra={"txn_ref": transaction.txn_ref},
            )
            return

        # Prepare email configuration and context
        config = template_map[transaction.status]
        context = {
            "customer_name": transaction.order.customer.full_name,
            "order_id": transaction.order.id,
            "amount": transaction.amount,
            "message": transaction.message or "Unknown error"
            if transaction.status == PaymentTransaction.StatusChoices.FAILED
            else None,
            "current_year": timezone.now().year,
        }
        html_content = render_to_string(config["template"], context)
        email = Email.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=transaction.order.customer.user.email,
            subject=config["subject"],
            plain_text=config["plain_text"],
            html=html_content,
            status=Email.Status.SENDING,
        )
        email_send(email)
        logger.info(
            "Email sent for payment transaction with status",
            extra={
                "txn_ref": transaction.txn_ref,
                "status": transaction.status,
            },
        )

    except Exception as e:
        logger.exception(
            "[ERROR] Payment email notification failed",
            extra={
                "error": str(e),
                "txn_ref": transaction.txn_ref,
                "status": transaction.status,
            },
        )
