# Create your models here.
from django.db import models

from rolt.common.models import BaseModel


class Email(BaseModel):
    class Status(models.TextChoices):
        READY = "READY", "Ready"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    status = models.CharField(
        max_length=255,
        db_index=True,
        choices=Status.choices,
        default=Status.READY,
    )

    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)

    html = models.TextField()
    plain_text = models.TextField()

    sent_at = models.DateTimeField(blank=True, null=True)
