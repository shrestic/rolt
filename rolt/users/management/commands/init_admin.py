import environ
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

env = environ.Env()


class Command(BaseCommand):
    help = "Create default superuser if not exists"

    def handle(self, *args, **kwargs):
        user = get_user_model()
        if not user.objects.filter(username="admin").exists():
            user.objects.create_superuser(
                username=env("ADMIN_USERNAME"),
                email=env("ADMIN_EMAIL"),
                password=env("ADMIN_PASSWORD"),
            )
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
