import asyncio
import json
import logging
import time

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message
from .models import Room

User = get_user_model()
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.last_active = time.time()
        self.timeout_seconds = 300  # 5 minutes

        # Start timeout watcher
        self.timeout_task = asyncio.create_task(self.watch_inactivity())
        # Join channel layer group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info(
            "[CONNECT] Client joined room",
            extra={
                "client": self.scope["client"],
                "room_name": self.room_name,
            },
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(
            "[DISCONNECT] Client left room",
            extra={
                "client": self.scope["client"],
                "room_name": self.room_name,
            },
        )
        if hasattr(self, "timeout_task"):
            self.timeout_task.cancel()

    async def receive(self, text_data):
        self.last_active = time.time()
        try:
            data = json.loads(text_data)
            content = data.get("message")
            user = self.scope["user"]

            if not user.is_authenticated:
                logger.warning("[AUTH] Unauthenticated user tried to send message")
                return

            # Unwrap lazy user object
            user = await sync_to_async(
                lambda: user.get_user() if hasattr(user, "get_user") else user,
            )()

            # Get chat room by name
            try:
                room = await database_sync_to_async(Room.objects.get)(
                    name=self.room_name,
                )
                # Check if room is active
                if not room.is_active:
                    logger.warning(
                        "[ROOM CLOSED] Attempt to send message to closed room",
                        extra={"room_name": room.name, "username": user.username},
                    )
                    await self.close()
                    return

            except Room.DoesNotExist:
                logger.exception(
                    "[ROOM] Room does not exist",
                    extra={"room_name": self.room_name},
                )
                return

            # Check if user has permission to send (must be customer or assigned_to)
            if user.id not in [room.customer_id, room.assigned_to_id]:
                logger.warning(
                    "[DENIED] User not allowed to send message in room",
                    extra={
                        "username": user.username,
                        "room_name": room.name,
                    },
                )
                return
            # Check if message is empty
            if not content or len(content.strip()) == 0:
                return  # ignore empty message

            # Save message to database
            await database_sync_to_async(Message.objects.create)(
                room=room,
                user=user,
                content=content,
            )

            # Broadcast to all users in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": content,
                    "user": user.username,
                },
            )

            logger.info(
                "[MESSAGE] User sent a message",
                extra={
                    "username": user.username,
                    "content": content,
                },
            )

        except json.JSONDecodeError as e:
            logger.exception("[JSON Decode Error]", extra={"exception": str(e)})
        except Room.DoesNotExist as e:
            logger.exception("[ChatRoom Error]", extra={"exception": str(e)})
        except Exception as e:  # Catch any other unexpected exceptions
            logger.exception("[Unexpected Error]", extra={"exception": str(e)})

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": event["user"],
                },
            ),
        )

    async def watch_inactivity(self):
        try:
            while True:
                await asyncio.sleep(10)  # Check every 10 seconds
                if time.time() - self.last_active > self.timeout_seconds:
                    # Send system message before closing
                    try:
                        await self.send(
                            text_data=json.dumps(
                                {
                                    "message": "You have been inactive for too long. Closing connection.",  # noqa: E501
                                    "user": "system",
                                },
                            ),
                        )
                    except Exception as send_error:  # noqa: BLE001
                        logger.warning(
                            "[INACTIVE] Could not notify before closing",
                            extra={"error": str(send_error)},
                        )

                    logger.info(
                        "[INACTIVE] Closing connection due to inactivity",
                        extra={
                            "channel": self.channel_name,
                            "user": str(self.scope.get("user")),
                        },
                    )
                    await self.close(code=4000)
                    break
        except asyncio.CancelledError:
            pass  # Task was cancelled, exit gracefully
        except Exception as e:
            logger.exception(
                "[INACTIVITY WATCHER ERROR] An error occurred in the inactivity watcher",  # noqa: E501
                extra={"exception": str(e)},
            )
