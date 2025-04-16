from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rolt.accounts.services.customer_service import CustomerService
from rolt.accounts.services.employee_service import EmployeeService


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        if user.is_staff:
            EmployeeService().employee_create(user=user)
        else:
            CustomerService().customer_create(user=user)
