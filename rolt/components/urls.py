from django.urls import include
from django.urls import path

from rolt.components.apis.kit_api import KitBulkCreateApi
from rolt.components.apis.kit_api import KitCreateApi
from rolt.components.apis.kit_api import KitDeleteApi
from rolt.components.apis.kit_api import KitDetailApi
from rolt.components.apis.kit_api import KitListApi
from rolt.components.apis.kit_api import KitUpdateApi

kit_patterns = [
    path("", KitListApi.as_view(), name="kit-list"),
    path("create/", KitCreateApi.as_view(), name="kit-create"),
    path(
        "bulk-create/",
        KitBulkCreateApi.as_view(),
        name="kit-bulk-create",
    ),
    path("<str:code>/", KitDetailApi.as_view(), name="kit-detail"),
    path(
        "<str:code>/update/",
        KitUpdateApi.as_view(),
        name="kit-update",
    ),
    path(
        "<str:code>/delete/",
        KitDeleteApi.as_view(),
        name="kit-delete",
    ),
]

urlpatterns = [
    path("kits/", include(kit_patterns), name="kits"),
]
