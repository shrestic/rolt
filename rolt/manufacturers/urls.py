from django.urls import path

from rolt.manufacturers.apis import ManufacturerBulkCreateApi
from rolt.manufacturers.apis import ManufacturerCreateApi
from rolt.manufacturers.apis import ManufacturerDeleteApi
from rolt.manufacturers.apis import ManufacturerDetailApi
from rolt.manufacturers.apis import ManufacturerListApi
from rolt.manufacturers.apis import ManufacturerUpdateApi

urlpatterns = [
    path("create/", ManufacturerCreateApi.as_view(), name="manufacturer-create"),
    path(
        "bulk-create/",
        ManufacturerBulkCreateApi.as_view(),
        name="manufacturer-bulk-create",
    ),
    path(
        "",
        ManufacturerListApi.as_view(),
        name="manufacturer-list",
    ),
    path(
        "<str:code>/",
        ManufacturerDetailApi.as_view(),
        name="manufacturer-detail",
    ),
    path(
        "<str:code>/update/",
        ManufacturerUpdateApi.as_view(),
        name="manufacturer-update",
    ),
    path(
        "<str:code>/delete/",
        ManufacturerDeleteApi.as_view(),
        name="manufacturer-delete",
    ),
]
