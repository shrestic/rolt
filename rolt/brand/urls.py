from django.urls import path

from rolt.brand.apis import BrandBulkCreateApi
from rolt.brand.apis import BrandCreateApi
from rolt.brand.apis import BrandDeleteApi
from rolt.brand.apis import BrandDetailApi
from rolt.brand.apis import BrandListApi
from rolt.brand.apis import BrandUpdateApi

urlpatterns = [
    path("create/", BrandCreateApi.as_view(), name="brand-create"),
    path("bulk-create/", BrandBulkCreateApi.as_view(), name="brand-bulk-create"),
    path("", BrandListApi.as_view(), name="brand-list"),
    path("<str:code>/", BrandDetailApi.as_view(), name="brand-detail"),
    path(
        "<str:code>/update/",
        BrandUpdateApi.as_view(),
        name="brand-update",
    ),
    path(
        "<str:code>/delete/",
        BrandDeleteApi.as_view(),
        name="brand-delete",
    ),
]
