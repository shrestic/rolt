from django.urls import include
from django.urls import path

from rolt.components.apis.keycap_api import KeycapBulkCreateApi
from rolt.components.apis.keycap_api import KeycapCreateApi
from rolt.components.apis.keycap_api import KeycapDeleteApi
from rolt.components.apis.keycap_api import KeycapDetailApi
from rolt.components.apis.keycap_api import KeycapListApi
from rolt.components.apis.keycap_api import KeycapUpdateApi
from rolt.components.apis.stabilizer_api import StabilizerBulkCreateApi
from rolt.components.apis.stabilizer_api import StabilizerCreateApi
from rolt.components.apis.stabilizer_api import StabilizerDeleteApi
from rolt.components.apis.stabilizer_api import StabilizerDetailApi
from rolt.components.apis.stabilizer_api import StabilizerListApi
from rolt.components.apis.stabilizer_api import StabilizerUpdateApi
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

stabilizer_patterns = [
    path("", StabilizerListApi.as_view(), name="stabilizer-list"),
    path("create/", StabilizerCreateApi.as_view(), name="stabilizer-create"),
    path(
        "bulk-create/",
        StabilizerBulkCreateApi.as_view(),
        name="stabilizer-bulk-create",
    ),
    path("<str:code>/", StabilizerDetailApi.as_view(), name="stabilizer-detail"),
    path("<str:code>/update/", StabilizerUpdateApi.as_view(), name="stabilizer-update"),
    path("<str:code>/delete/", StabilizerDeleteApi.as_view(), name="stabilizer-delete"),
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
    path("switches/", include((switch_patterns, "switches"))),
    path("stabilizers/", include((stabilizer_patterns, "stabilizers"))),
    path("keycaps/", include((keycap_patterns, "keycaps"))),
]
