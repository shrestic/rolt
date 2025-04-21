from django.urls import include
from django.urls import path

from rolt.components.apis.keycap_apis import KeycapBulkCreateApi
from rolt.components.apis.keycap_apis import KeycapCreateApi
from rolt.components.apis.keycap_apis import KeycapDeleteApi
from rolt.components.apis.keycap_apis import KeycapDetailApi
from rolt.components.apis.keycap_apis import KeycapListApi
from rolt.components.apis.keycap_apis import KeycapUpdateApi
from rolt.components.apis.kit_apis import KitBulkCreateApi
from rolt.components.apis.kit_apis import KitCreateApi
from rolt.components.apis.kit_apis import KitDeleteApi
from rolt.components.apis.kit_apis import KitDetailApi
from rolt.components.apis.kit_apis import KitListApi
from rolt.components.apis.kit_apis import KitUpdateApi
from rolt.components.apis.switch_apis import SwitchBulkCreateApi
from rolt.components.apis.switch_apis import SwitchCreateApi
from rolt.components.apis.switch_apis import SwitchDeleteApi
from rolt.components.apis.switch_apis import SwitchDetailApi
from rolt.components.apis.switch_apis import SwitchListApi
from rolt.components.apis.switch_apis import SwitchUpdateApi

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


switch_patterns = [
    path("", SwitchListApi.as_view(), name="switch-list"),
    path("create/", SwitchCreateApi.as_view(), name="switch-create"),
    path("bulk-create/", SwitchBulkCreateApi.as_view(), name="switch-bulk-create"),
    path("<str:code>/", SwitchDetailApi.as_view(), name="switch-detail"),
    path("<str:code>/update/", SwitchUpdateApi.as_view(), name="switch-update"),
    path("<str:code>/delete/", SwitchDeleteApi.as_view(), name="switch-delete"),
]

keycap_patterns = [
    path("", KeycapListApi.as_view(), name="keycap-list"),
    path("create/", KeycapCreateApi.as_view(), name="keycap-create"),
    path("bulk-create/", KeycapBulkCreateApi.as_view(), name="keycap-bulk-create"),
    path("<str:code>/", KeycapDetailApi.as_view(), name="keycap-detail"),
    path("<str:code>/update/", KeycapUpdateApi.as_view(), name="keycap-update"),
    path("<str:code>/delete/", KeycapDeleteApi.as_view(), name="keycap-delete"),
]


urlpatterns = [
    path("kits/", include(kit_patterns), name="kits"),
    path("switches/", include(switch_patterns), name="switches"),
    path("keycaps/", include(keycap_patterns), name="keycaps"),
]
