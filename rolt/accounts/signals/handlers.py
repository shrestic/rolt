from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from rolt.accounts.services.customer_service import CustomerService
from rolt.accounts.services.employee_service import EmployeeService

User = get_user_model()


@receiver(post_save, sender=User)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        if user.is_staff:
            EmployeeService().employee_create(user=user)
        else:
            CustomerService().customer_create(user=user)
            group, _ = Group.objects.get_or_create(name="Customer")
            user.groups.add(group)
