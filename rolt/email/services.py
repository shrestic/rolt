import secrets

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils import timezone

from rolt.common.services import model_update
from rolt.core.exceptions import ApplicationError
from rolt.email.models import Email
from rolt.email.tasks import email_send as email_send_task


@transaction.atomic
def email_failed(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        msg = f"Cannot fail non-sending emails. Current status is {email.status}"
        raise ApplicationError(message=msg)

    email, _ = model_update(
        instance=email,
        fields=["status"],
        data={"status": Email.Status.FAILED},
    )
    return email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        msg = f"Cannot send non-ready emails. Current status is {email.status}"
        raise ApplicationError(message=msg)

    if settings.EMAIL_SENDING_FAILURE_TRIGGER:
        failure_dice = secrets.SystemRandom().uniform(0, 1)

        if failure_dice <= settings.EMAIL_SENDING_FAILURE_RATE:
            msg = "Email sending failure triggered."
            raise ApplicationError(message=msg)

    subject = email.subject
    sender = email.sender
    recipient = email.recipient

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, sender, [recipient])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={"status": Email.Status.SENT, "sent_at": timezone.now()},
    )
    return email


def email_send_all(emails: QuerySet[Email]):
    """
    This is a very specific service.

    We don't want to decorate with @transaction.atomic,
    since we are executing updates, 1 by 1, in a separate atomic block,
    so we can trigger transaction.on_commit for each email, separately.
    """
    for email in emails:
        with transaction.atomic():
            Email.objects.filter(id=email.id).update(status=Email.Status.SENDING)

        # Create a closure, to capture the proper value of each id
        transaction.on_commit(lambda email_id=email.id: email_send_task.delay(email_id))
