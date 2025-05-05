from celery import shared_task
from django.utils import timezone

from rolt.warranty.models import Warranty
from rolt.warranty.services import warranty_mark_expired


@shared_task
def update_expired_warranties():
    today = timezone.now().date()
    active_warranties = Warranty.objects.filter(
        status=Warranty.Status.ACTIVE,
        end_date__lte=today,
    )

    for warranty in active_warranties:
        warranty_mark_expired(instance=warranty)
