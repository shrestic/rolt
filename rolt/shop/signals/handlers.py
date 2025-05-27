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


def format_vnd(amount):
    return f"{int(amount):,} VND".replace(",", ".")


@receiver(post_save, sender=Order)
def send_order_notification_email(instance, **_):
    order: Order = instance

    try:
        if order.status == Order.StatusChoices.PENDING and order.total_amount == 0:
            logger.debug("Skipping email for zero-amount PENDING order %s", order.id)
            return

        template_map = {
            Order.StatusChoices.PENDING: {
                "subject": f"[Rolt] Order Confirmation #{order.id}",
                "template": "email/pending_order_notify.html",
                "plain_text": (
                    f"Hi {order.customer.full_name},\n\n"
                    f"Thank you for your order!\n"
                    f"Order ID: {order.id}\n"
                    f"Status: {order.get_status_display()}\n"
                    f"Total: {format_vnd(order.total_amount)}\n"
                    f"Placed at: {localtime(order.created_at).strftime('%Y-%m-%d %H:%M')}\n"  # noqa: E501
                ),
            },
            Order.StatusChoices.PAID: {
                "subject": f"[Rolt] Payment Successful - Order #{order.id}",
                "template": "email/paid_order_notify.html",
                "plain_text": (
                    f"Hi {order.customer.full_name},\n\n"
                    f"Your payment for Order #{order.id} has been confirmed.\n"
                    f"Total: {format_vnd(order.total_amount)}\n"
                    f"Placed at: {localtime(order.created_at).strftime('%Y-%m-%d %H:%M')}\n"  # noqa: E501
                ),
            },
            Order.StatusChoices.CANCELLED: {
                "subject": f"[Rolt] Order #{order.id} Cancelled",
                "template": "email/cancelled_order_notify.html",
                "plain_text": (
                    f"Hi {order.customer.full_name},\n\n"
                    f"Your order #{order.id} has been cancelled.\n"
                    f"Total: {format_vnd(order.total_amount)}\n"
                    f"If you have questions, please contact support.\n"
                ),
            },
            Order.StatusChoices.REFUNDED: {
                "subject": f"[Rolt] Refund Processed - Order #{order.id}",
                "template": "email/refunded_order_notify.html",
                "plain_text": (
                    f"Hi {order.customer.full_name},\n\n"
                    f"Your refund for Order #{order.id} has been processed.\n"
                    f"Refund Amount: {format_vnd(order.total_amount)}\n"
                    f"Refunded at: {localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')}\n"  # noqa: E501
                ),
            },
        }

        if order.status not in template_map:
            logger.debug(
                "No email template for status %s of order %s",
                order.status,
                order.id,
            )
            return

        items = OrderItem.objects.select_related("content_type").filter(order=order)
        for item in items:
            item.display_price = format_vnd(item.price_snapshot)
        config = template_map[order.status]

        context = {
            "customer_name": order.customer.full_name,
            "order_id": order.id,
            "status": order.get_status_display(),
            "total_amount": format_vnd(order.total_amount),
            "created_at": localtime(order.created_at).strftime("%Y-%m-%d %H:%M"),
            "items": items,
            "current_year": timezone.now().year,
        }

        html = render_to_string(config["template"], context)

        email = Email.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=order.customer.user.email,
            subject=config["subject"],
            plain_text=config["plain_text"],
            html=html,
            status=Email.Status.SENDING,
        )
        email_send(email)

        logger.info("Order email sent for order %s [%s]", order.id, order.status)

    except Exception as e:
        logger.exception(
            "[ERROR] Order email failed",
            extra={"error": str(e), "order_id": order.id, "status": order.status},
        )


@receiver(post_save, sender=PaymentTransaction)
def send_payment_notification_email(sender, instance, created, **kwargs):
    txn: PaymentTransaction = instance

    try:
        if not txn.order:
            logger.debug("No order linked with txn_ref %s", txn.txn_ref)
            return

        if txn.status != PaymentTransaction.StatusChoices.FAILED:
            return

        config = {
            "subject": f"[Rolt] Payment Failed - Order #{txn.order.id}",
            "template": "email/failed_payment_notify.html",
            "plain_text": (
                f"Hi {txn.order.customer.full_name},\n\n"
                f"Your payment attempt for Order #{txn.order.id} has failed.\n"
                f"Amount: {format_vnd(txn.amount)}\n"
                f"Reason: {txn.message or 'Unknown error'}\n"
            ),
        }

        context = {
            "customer_name": txn.order.customer.full_name,
            "order_id": txn.order.id,
            "amount": format_vnd(txn.amount),
            "message": txn.message or "Unknown error",
            "current_year": timezone.now().year,
        }

        html = render_to_string(config["template"], context)

        email = Email.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=txn.order.customer.user.email,
            subject=config["subject"],
            plain_text=config["plain_text"],
            html=html,
            status=Email.Status.SENDING,
        )
        email_send(email)
        logger.info("Payment failure email sent for txn_ref %s", txn.txn_ref)

    except Exception as e:
        logger.exception(
            "[ERROR] Payment email failed",
            extra={"error": str(e), "txn_ref": txn.txn_ref, "status": txn.status},
        )
