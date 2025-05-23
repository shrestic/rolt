import uuid

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

from rolt.accounts.validators import UserValidator
from rolt.common.models import BaseModel
from rolt.core.validators import validate_file_size

PHONE_LENGTH = 10

User = get_user_model()


# Create your models here.
class Customer(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=PHONE_LENGTH, default="", blank=True)
    address = models.TextField(default="", blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(
        upload_to="customer/images",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
    )

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def clean(self):
        UserValidator().validate_birth_date(self.birth_date)
        UserValidator().validate_phone(self.phone)
        UserValidator().validate_file_size(self.image)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        db_table = "customer"
