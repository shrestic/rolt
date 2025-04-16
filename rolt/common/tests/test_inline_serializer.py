from datetime import UTC
from datetime import datetime

from rest_framework import serializers

from rolt.common.utils import inline_serializer
from rolt.common.utils import make_mock_object


def test_if_inline_serializer_is_created_correctly():
    # Arrange
    dt = datetime(
        year=2021,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        microsecond=1,
        tzinfo=UTC,
    )
    expected_dt = "2021-01-01T01:01:01.000001Z"
    obj = make_mock_object(foo=1, bar="bar", dt=dt)

    serializer = inline_serializer(
        fields={
            "foo": serializers.IntegerField(),
            "bar": serializers.CharField(),
            "dt": serializers.DateTimeField(),
        },
    )

    # Act & Assert (Output)  # noqa: ERA001
    result = serializer.to_representation(obj)
    expected = {"foo": 1, "bar": "bar", "dt": expected_dt}
    assert result == expected

    # Act & Assert (Input)  # noqa: ERA001
    payload = {"foo": 1, "bar": "bar", "dt": expected_dt}
    result = serializer.to_internal_value(payload)
    expected = {"foo": 1, "bar": "bar", "dt": dt}
    assert result == expected


def test_if_inline_serializer_is_created_correctly_with_many_true():
    # Arrange
    obj = make_mock_object(foo=1)
    serializer = inline_serializer(
        many=True,
        fields={
            "foo": serializers.IntegerField(),
        },
    )
    objects = [obj]

    # Act & Assert (Output)  # noqa: ERA001
    result = serializer.to_representation(objects)
    expected = [{"foo": 1}]
    assert result == expected

    # Act & Assert (Input)  # noqa: ERA001
    payload = [{"foo": 1}]
    result = serializer.to_internal_value(payload)
    expected = [{"foo": 1}]
    assert result == expected
