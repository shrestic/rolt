from django.urls import path

from rolt.builds.apis import BuildCreateApi
from rolt.builds.apis import BuildDeleteApi
from rolt.builds.apis import BuildUpdateApi
from rolt.builds.apis import CustomerBuildDetailApi
from rolt.builds.apis import CustomerBuildListApi
from rolt.builds.apis import PresetBuildDetailApi
from rolt.builds.apis import PresetBuildListApi

urlpatterns = [
    # Preset builds (system-wide)
    path("presets/", PresetBuildListApi.as_view(), name="preset-build-list"),
    path(
        "presets/<uuid:build_id>/",
        PresetBuildDetailApi.as_view(),
        name="preset-build-detail",
    ),
    # Customer builds (owned by users)
    path("customer/", CustomerBuildListApi.as_view(), name="customer-build-list"),
    path(
        "customer/<uuid:build_id>/",
        CustomerBuildDetailApi.as_view(),
        name="customer-build-detail",
    ),
    # Shared endpoint
    path("create/", BuildCreateApi.as_view(), name="build-create"),
    path(
        "<uuid:pk>/update/",
        BuildUpdateApi.as_view(),
        name="build-update",
    ),
    path("<uuid:pk>/delete/", BuildDeleteApi.as_view(), name="build-delete"),
]
