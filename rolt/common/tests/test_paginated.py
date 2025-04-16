from collections import OrderedDict
from unittest.mock import patch

import pytest
from django.test.utils import override_settings
from django.urls import path
from model_bakery import baker
from rest_framework import serializers
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from rolt.common.models import SimpleModel
from rolt.common.pagination import LimitOffsetPagination
from rolt.common.pagination import get_paginated_response


# -------------------------------
# Fake view & routing for testing
# -------------------------------
class ExampleListApi(APIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SimpleModel
            fields = ("id", "name")

    def get(self, request):
        queryset = SimpleModel.objects.order_by("id")
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )


urlpatterns = [
    path("some/path/", ExampleListApi.as_view(), name="example-list"),
]


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def simple_objects():
    obj1, obj2 = baker.make(SimpleModel, _quantity=2)
    return sorted([obj1, obj2], key=lambda x: x.id)


# -------------------------------
# Tests
# -------------------------------
@override_settings(ROOT_URLCONF=__name__)
@pytest.mark.django_db
def test_if_response_is_paginated_return_200(api_client, authenticate, simple_objects):
    # Arrange
    authenticate()
    obj1, obj2 = simple_objects

    # Act page 1
    response_1 = api_client.get("/some/path/")

    # Assert page 1
    assert response_1.status_code == status.HTTP_200_OK
    assert response_1.data == OrderedDict(
        {
            "limit": 1,
            "offset": 0,
            "count": 2,
            "next": "http://testserver/some/path/?limit=1&offset=1",
            "previous": None,
            "results": [{"id": obj1.id, "name": obj1.name}],
        },
    )

    # Act page 2
    response_2 = api_client.get("/some/path/?limit=1&offset=1")

    # Assert page 2
    assert response_2.status_code == status.HTTP_200_OK
    assert response_2.data == OrderedDict(
        {
            "limit": 1,
            "offset": 1,
            "count": 2,
            "next": None,
            "previous": "http://testserver/some/path/?limit=1",
            "results": [{"id": obj2.id, "name": obj2.name}],
        },
    )


@override_settings(ROOT_URLCONF=__name__)
@pytest.mark.django_db
def test_if_response_is_no_paginated_return_200(
    api_client,
    authenticate,
    simple_objects,
):
    # Arrange
    authenticate()

    with patch(
        "rolt.common.pagination.LimitOffsetPagination.paginate_queryset",
        return_value=None,
    ):
        # Act
        response = api_client.get("/some/path/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "results" not in response.data
    assert isinstance(response.data, (list, dict))
