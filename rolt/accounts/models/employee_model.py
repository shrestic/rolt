import uuid

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

from rolt.accounts.validators import UserValidator
from rolt.common.models import BaseModel

PHONE_LENGTH = 10

User = get_user_model()


# Create your models here.
class Employee(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
    )
    phone = models.CharField(max_length=PHONE_LENGTH, default="", blank=True)
    address = models.TextField(default="", blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=255, default="", blank=True)
    department = models.CharField(max_length=255, default="", blank=True)
    start_date = models.DateField(null=True, blank=True)

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

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employee"
