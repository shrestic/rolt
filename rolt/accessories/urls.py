from django.urls import path

from rolt.accessories.apis import AccessoryCreateApi
from rolt.accessories.apis import AccessoryDeleteApi
from rolt.accessories.apis import AccessoryDetailApi
from rolt.accessories.apis import AccessoryListApi
from rolt.accessories.apis import AccessoryUpdateApi

urlpatterns = [
    path("", AccessoryListApi.as_view(), name="accessory-list"),
    path("create/", AccessoryCreateApi.as_view(), name="accessory-create"),
    path(
        "<uuid:pk>/",
        AccessoryDetailApi.as_view(),
        name="accessory-detail",
    ),
    path(
        "<uuid:pk>/update/",
        AccessoryUpdateApi.as_view(),
        name="accessory-update",
    ),
    path(
        "<uuid:pk>/delete/",
        AccessoryDeleteApi.as_view(),
        name="accessory-delete",
    ),
]
