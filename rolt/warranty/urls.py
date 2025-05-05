from django.urls import path

from rolt.warranty.apis import WarrantyDeleteApi
from rolt.warranty.apis import WarrantyDetailApi
from rolt.warranty.apis import WarrantyListApi
from rolt.warranty.apis import WarrantyMarkExpiredApi
from rolt.warranty.apis import WarrantyRequestAllListApi
from rolt.warranty.apis import WarrantyRequestApproveApi
from rolt.warranty.apis import WarrantyRequestCreateApi
from rolt.warranty.apis import WarrantyRequestDetailApi
from rolt.warranty.apis import WarrantyRequestListApi
from rolt.warranty.apis import WarrantyRequestRejectApi
from rolt.warranty.apis import WarrantyVoidApi

urlpatterns = [
    path("", WarrantyListApi.as_view(), name="warranty-list"),
    path("<uuid:pk>/", WarrantyDetailApi.as_view(), name="warranty-detail"),
    path("<uuid:pk>/void/", WarrantyVoidApi.as_view(), name="warranty-void"),
    path("<uuid:pk>/expire/", WarrantyMarkExpiredApi.as_view(), name="warranty-expire"),
    path("<uuid:pk>/delete/", WarrantyDeleteApi.as_view(), name="warranty-delete"),
    path(
        "request/create/",
        WarrantyRequestCreateApi.as_view(),
        name="warranty-request-create",
    ),
    path("request/", WarrantyRequestListApi.as_view(), name="warranty-request-list"),
    path(
        "request/<uuid:pk>/",
        WarrantyRequestDetailApi.as_view(),
        name="warranty-request-detail",
    ),
    path(
        "request/all/",
        WarrantyRequestAllListApi.as_view(),
        name="warranty-request-all-list",
    ),
    path(
        "request/<uuid:pk>/approve/",
        WarrantyRequestApproveApi.as_view(),
        name="warranty-request-approve",
    ),
    path(
        "request/<uuid:pk>/reject/",
        WarrantyRequestRejectApi.as_view(),
        name="warranty-request-reject",
    ),
]
