from django.urls import include
from django.urls import path

from rolt.components.apis.keycap_api import KeycapBulkCreateApi
from rolt.components.apis.keycap_api import KeycapCreateApi
from rolt.components.apis.keycap_api import KeycapDeleteApi
from rolt.components.apis.keycap_api import KeycapDetailApi
from rolt.components.apis.keycap_api import KeycapListApi
from rolt.components.apis.keycap_api import KeycapUpdateApi
from rolt.components.apis.kit_api import KitBulkCreateApi
from rolt.components.apis.kit_api import KitCreateApi
from rolt.components.apis.kit_api import KitDeleteApi
from rolt.components.apis.kit_api import KitDetailApi
from rolt.components.apis.kit_api import KitListApi
from rolt.components.apis.kit_api import KitUpdateApi
from rolt.components.apis.switch_api import SwitchBulkCreateApi
from rolt.components.apis.switch_api import SwitchCreateApi
from rolt.components.apis.switch_api import SwitchDeleteApi
from rolt.components.apis.switch_api import SwitchDetailApi
from rolt.components.apis.switch_api import SwitchListApi
from rolt.components.apis.switch_api import SwitchUpdateApi

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
