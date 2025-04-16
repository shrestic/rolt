from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

GROUP_NAMES = [
    "Customer",
    "Technician",
    "Support",
    "Product Manager",
    "Finance",
    "Content Designer",
]


class Command(BaseCommand):
    help = "Create default user groups for keyboard platform"

    def handle(self, *args, **kwargs):
        for group_name in GROUP_NAMES:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Group already exists: {group_name}"),
                )

        self.stdout.write(self.style.SUCCESS("All default groups initialized."))
