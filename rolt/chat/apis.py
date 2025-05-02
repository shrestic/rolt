from rest_framework import generics
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from rolt.chat.models import Room
from rolt.core.permissions import IsCustomer


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["name"]


class ChatRoomCreateApi(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = ChatRoomCreateSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "chat_room_create"

    def perform_create(self, serializer):
        existing_active_room = Room.objects.filter(
            customer=self.request.user,
            is_active=True,
        ).first()

        if existing_active_room:
            raise ValidationError(
                {
                    "detail": "You already have an open chat room.",
                    "room": {
                        "id": existing_active_room.id,
                        "name": existing_active_room.name,
                    },
                },
            )

        serializer.save(customer=self.request.user)
