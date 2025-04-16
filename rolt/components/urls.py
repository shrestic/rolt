from django.urls import include
from django.urls import path

from rolt.components.apis.switch_api import SwitchBulkCreateApi
from rolt.components.apis.switch_api import SwitchCreateApi
from rolt.components.apis.switch_api import SwitchDeleteApi
from rolt.components.apis.switch_api import SwitchDetailApi
from rolt.components.apis.switch_api import SwitchListApi
from rolt.components.apis.switch_api import SwitchUpdateApi

switch_patterns = [
    path("create/", SwitchCreateApi.as_view(), name="switch-create"),
    path(
        "bulk-create/",
        SwitchBulkCreateApi.as_view(),
        name="switch-bulk-create",
    ),
    path("", SwitchListApi.as_view(), name="switch-list"),
    path("<str:code>/", SwitchDetailApi.as_view(), name="switch-detail"),
    path(
        "<str:code>/update/",
        SwitchUpdateApi.as_view(),
        name="switch-update",
    ),
    path(
        "<str:code>/delete/",
        SwitchDeleteApi.as_view(),
        name="switch-delete",
    ),
]

urlpatterns = [
    path("switches/", include((switch_patterns, "switches"))),
]
