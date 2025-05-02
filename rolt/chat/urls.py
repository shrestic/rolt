from django.urls import path

from rolt.chat.apis import ChatRoomCreateApi

urlpatterns = [
    path("rooms/", ChatRoomCreateApi.as_view(), name="chatroom-create"),
]
