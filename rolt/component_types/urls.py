from django.urls import path

from rolt.component_types.apis import ComponentTypeCreateApi
from rolt.component_types.apis import ComponentTypeDeleteApi
from rolt.component_types.apis import ComponentTypeDetailApi
from rolt.component_types.apis import ComponentTypeListApi
from rolt.component_types.apis import ComponentTypeUpdateApi

urlpatterns = [
    path("create/", ComponentTypeCreateApi.as_view(), name="component-type-create"),
    path("", ComponentTypeListApi.as_view(), name="component-type-list"),
    path("<str:code>/", ComponentTypeDetailApi.as_view(), name="component-type-detail"),
    path(
        "<str:code>/update/",
        ComponentTypeUpdateApi.as_view(),
        name="component-type-update",
    ),
    path(
        "<str:code>/delete/",
        ComponentTypeDeleteApi.as_view(),
        name="component-type-delete",
    ),
]
