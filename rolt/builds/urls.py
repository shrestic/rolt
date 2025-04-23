from django.urls import path

from rolt.builds.apis.build_apis import BuildCreateApi
from rolt.builds.apis.build_apis import BuildDeleteApi
from rolt.builds.apis.build_apis import BuildUpdateApi
from rolt.builds.apis.build_apis import CustomerBuildDetailApi
from rolt.builds.apis.build_apis import CustomerBuildListApi
from rolt.builds.apis.build_apis import PresetBuildDetailApi
from rolt.builds.apis.build_apis import PresetBuildListApi
from rolt.builds.apis.services_apis import ServiceCreateApi
from rolt.builds.apis.services_apis import ServiceDeleteApi
from rolt.builds.apis.services_apis import ServiceListApi
from rolt.builds.apis.services_apis import ServiceUpdateApi
from rolt.builds.apis.showcase_apis import ShowcaseAddApi
from rolt.builds.apis.showcase_apis import ShowcaseDeleteApi
from rolt.builds.apis.showcase_apis import ShowcaseListApi

urlpatterns = [
    # -------------------------
    # Preset builds (public builds managed by admins)
    # -------------------------
    path("presets/", PresetBuildListApi.as_view(), name="preset-build-list"),
    path(
        "presets/<uuid:build_id>/",
        PresetBuildDetailApi.as_view(),
        name="preset-build-detail",
    ),
    # -------------------------
    # Customer builds (private builds owned by users)
    # -------------------------
    path("my/", CustomerBuildListApi.as_view(), name="customer-build-list"),
    path(
        "my/<uuid:build_id>/",
        CustomerBuildDetailApi.as_view(),
        name="my-build-detail",
    ),
    # -------------------------
    # Create / Update / Delete builds (shared endpoint for both customer & preset)
    # -------------------------
    path("create/", BuildCreateApi.as_view(), name="build-create"),
    path("<uuid:pk>/update/", BuildUpdateApi.as_view(), name="build-update"),
    path("<uuid:pk>/delete/", BuildDeleteApi.as_view(), name="build-delete"),
    # -------------------------
    # Showcase APIs (display featured preset builds)
    # -------------------------
    path("showcases/", ShowcaseListApi.as_view(), name="showcase-list"),
    path("showcases/create/", ShowcaseAddApi.as_view(), name="showcase-create"),
    path(
        "showcases/<uuid:pk>/delete/",
        ShowcaseDeleteApi.as_view(),
        name="showcase-delete",
    ),
    # -------------------------
    # Services APIs (display available services for builds)
    # -------------------------
    path("services/", ServiceListApi.as_view(), name="service-list"),
    path("services/create/", ServiceCreateApi.as_view(), name="service-create"),
    path(
        "services/<str:code>/update/",
        ServiceUpdateApi.as_view(),
        name="showcase-update",
    ),
    path(
        "services/<str:code>/delete/",
        ServiceDeleteApi.as_view(),
        name="service-delete",
    ),
]
