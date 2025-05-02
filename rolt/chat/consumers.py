import asyncio
import json
import logging
import time

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now

from rolt.email.models import Email
from rolt.email.services import email_send

from .models import Message
from .models import Room

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    TIMEOUT_SECONDS = 300

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.last_active = time.time()
        self.timeout_task = asyncio.create_task(self.watch_inactivity())

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info(
            "[CONNECT] Joined",
            extra={"room_name": self.room_name, "client": self.scope["client"]},
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if hasattr(self, "timeout_task"):
            self.timeout_task.cancel()
        logger.info(
            "[DISCONNECT] Left",
            extra={"room_name": self.room_name, "client": self.scope["client"]},
        )

    async def receive(self, text_data):
        self.last_active = time.time()

        try:
            data = json.loads(text_data)
            content = data.get("message", "").strip()
            raw_user = self.scope["user"]
            user = (
                await sync_to_async(raw_user.get_user)
                if hasattr(raw_user, "get_user")
                else raw_user
            )

            if not user.is_authenticated or not content:
                return

            room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
            if not room.is_active or user.id not in [
                room.customer_id,
                room.assigned_to_id,
            ]:
                return

            await database_sync_to_async(Message.objects.create)(
                room=room,
                user=user,
                content=content,
            )

            if room.assigned_to_id is None:
                await self.notify_unassigned(room, user, content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": content, "user": user.username},
            )
            logger.info(
                "[MESSAGE] Sent",
                extra={"user": user.username, "content": content},
            )

        except Exception as e:
            logger.exception("[ERROR] Unexpected", extra={"exception": str(e)})

    async def notify_unassigned(self, room, user, content):
        html = render_to_string(
            "email/chat_message_notify.html",
            {
                "user_email": user.email,
                "content": content,
                "room_name": room.name,
                "current_year": now().year,
            },
        )
        email = await database_sync_to_async(Email.objects.create)(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=settings.SUPPORT_ALERT_EMAIL,
            subject=f"[New Chat] {user.email} started a conversation",
            plain_text=f"{user.email} messaged in room '{room.name}':\n\n{content}",
            html=html,
            status=Email.Status.SENDING,
        )
        await sync_to_async(email_send)(email)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def watch_inactivity(self):
        try:
            while True:
                await asyncio.sleep(10)
                if time.time() - self.last_active > self.TIMEOUT_SECONDS:
                    try:
                        await self.send(
                            text_data=json.dumps(
                                {
                                    "message": "Connection closed due to inactivity.",
                                    "user": "system",
                                },
                            ),
                        )
                    except Exception as e:  # noqa: BLE001
                        logger.warning(
                            "[INACTIVE] Failed to send notice",
                            extra={"error": str(e)},
                        )

                    await self.close(code=4000)
                    logger.info(
                        "[INACTIVE] Closed idle connection",
                        extra={"user": str(self.scope.get("user"))},
                    )
                    break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.exception("[INACTIVITY ERROR]", extra={"exception": str(e)})
