import uuid

from django.db import models

from rolt.common.models import BaseModel
from rolt.shop.models.order_model import Order


class PaymentTransaction(BaseModel):
    # Define payment method choices
    class MethodChoices(models.TextChoices):
        VNPAY = "vnpay", "VNPAY"

    # Define payment status choices
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    # Unique identifier for the payment transaction
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Reference to the associated order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # Unique transaction reference sent to VNPAY
    txn_ref = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique transaction code sent to VNPAY (vnp_TxnRef)",
    )

    # Payment method used
    method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices,
        default=MethodChoices.VNPAY,
    )

    # Current status of the payment transaction
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    # Payment amount in VND
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Order amount (VND)",
    )

    # Bank code that processed the transaction
    bank_code = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Bank code that processed the transaction (vnp_BankCode)",
    )

    # Transaction number provided by VNPAY
    vnpay_transaction_no = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Transaction number from VNPAY (vnp_TransactionNo)",
    )

    # Response code from VNPAY
    response_code = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="Response code from VNPAY (vnp_ResponseCode)",
    )

    # Additional message or notes about the payment
    message = models.TextField(
        blank=True,
        default="",
        help_text="Payment message/notes",
    )

    # Timestamp when the payment was completed
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "payment_transaction"
        ordering = ["-created_at"]
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"

    def __str__(self):
        return f"[{self.txn_ref}] {self.status.upper()} - {self.amount} VND"
