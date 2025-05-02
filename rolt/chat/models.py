from django.contrib.auth import get_user_model
from django.db import models

from rolt.common.models import BaseModel

User = get_user_model()


class Room(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="chat_rooms",
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_chat_rooms",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Message(BaseModel):
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}"
