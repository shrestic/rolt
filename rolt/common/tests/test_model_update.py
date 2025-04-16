from datetime import timedelta
from unittest.mock import patch

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from rolt.common.factories import RandomModelFactory
from rolt.common.factories import SimpleModelFactory
from rolt.common.models import TimestampsOpinionated
from rolt.common.services import model_update


@pytest.mark.django_db
def test_if_model_update_does_nothing_when_fields_are_empty():
    """
    Test that `model_update()` does nothing when no fields and no data are provided.
    This ensures that if both `fields=[]` and `data={}`, the model remains unchanged
    and the result should indicate no update.
    """
    instance = RandomModelFactory()
    updated_instance, has_updated = model_update(instance=instance, fields=[], data={})

    assert updated_instance == instance
    assert has_updated is False


@pytest.mark.django_db
def test_if_model_update_does_nothing_when_fields_not_in_data():
    """
    Test that `model_update()` does nothing if fields are specified,
    but those fields do not exist in the data dictionary.
    """
    instance = RandomModelFactory()
    updated_instance, has_updated = model_update(
        instance=instance,
        fields=["start_date"],
        data={"foo": "bar"},
    )

    assert updated_instance == instance
    assert has_updated is False


@pytest.mark.django_db
def test_if_model_update_updates_only_passed_fields_from_data():
    """
    Test that `model_update()` only updates fields explicitly listed in `fields`,
    even if the `data` dictionary includes more keys.
    Also verifies that the generated SQL query only updates the intended field(s).
    """
    instance = RandomModelFactory()
    update_fields = ["start_date"]
    data = {
        "field_a": "value_a",
        "start_date": instance.start_date - timedelta(days=1),
        "end_date": instance.end_date + timedelta(days=1),
    }

    assert instance.start_date != data["start_date"]

    with CaptureQueriesContext(connection) as ctx:
        updated_instance, has_updated = model_update(
            instance=instance,
            fields=update_fields,
            data=data,
        )
        update_query = ctx.captured_queries[-1]

    assert has_updated is True
    assert updated_instance.start_date == data["start_date"]
    assert updated_instance.end_date != data["end_date"]
    assert not hasattr(updated_instance, "field_a")
    assert "end_date" not in update_query["sql"]


@pytest.mark.django_db
def test_if_model_update_raises_error_when_field_does_not_exist():
    """
    Test that `model_update()` raises an AssertionError when a non-existent
    field is provided. Helps catch typos or invalid keys early.
    """
    instance = RandomModelFactory()
    with pytest.raises(AssertionError):
        model_update(
            instance=instance,
            fields=["non_existing_field"],
            data={"non_existing_field": "value"},
        )


@pytest.mark.django_db
def test_if_model_update_updates_many_to_many_fields():
    """
    Test that `model_update()` can update ManyToMany fields correctly,
    and that it does NOT auto-update the `updated_at` field.
    """
    instance = RandomModelFactory()
    simple_obj = SimpleModelFactory()

    assert simple_obj not in instance.simple_objects.all()
    original_updated_at = instance.updated_at

    updated_instance, has_updated = model_update(
        instance=instance,
        fields=["simple_objects"],
        data={"simple_objects": [simple_obj]},
    )

    assert has_updated is True
    assert updated_instance == instance
    assert simple_obj in updated_instance.simple_objects.all()
    assert updated_instance.updated_at == original_updated_at


@pytest.mark.django_db
def test_if_model_update_updates_m2m_and_standard_fields():
    """
    Test that `model_update()` supports updating both standard fields
    and ManyToMany fields in a single call.
    """
    instance = RandomModelFactory()
    simple_obj = SimpleModelFactory()

    assert simple_obj not in instance.simple_objects.all()

    data = {
        "start_date": instance.start_date - timedelta(days=1),
        "simple_objects": [simple_obj],
    }

    updated_instance, has_updated = model_update(
        instance=instance,
        fields=["start_date", "simple_objects"],
        data=data,
    )

    assert has_updated is True
    assert updated_instance.start_date == data["start_date"]
    assert simple_obj in updated_instance.simple_objects.all()


@pytest.mark.django_db
def test_if_model_update_sets_updated_at_automatically_if_not_provided():
    """
    Test that if the model has an `updated_at` field and it's not passed in `data`,
    `model_update()` will automatically set it to `timezone.now()`.
    """
    instance = TimestampsOpinionated()
    instance.full_clean()
    instance.save()

    assert instance.updated_at is None

    updated_instance, has_updated = model_update(
        instance=instance,
        fields=["created_at"],
        data={"created_at": timezone.now() - timedelta(days=1)},
    )

    assert has_updated is True
    assert updated_instance.updated_at is not None


@pytest.mark.django_db
def test_if_model_update_respects_provided_updated_at():
    """
    Test that `model_update()` respects the `updated_at` value provided in the `data`
    and does not override it with `timezone.now()`.
    """
    instance = TimestampsOpinionated()
    instance.full_clean()
    instance.save()

    updated_at = timezone.now()

    updated_instance, has_updated = model_update(
        instance=instance,
        fields=["updated_at"],
        data={"updated_at": updated_at},
    )

    assert has_updated is True
    assert updated_instance.updated_at == updated_at


@pytest.mark.django_db
def test_if_model_update_does_not_update_updated_at_when_auto_updated_at_false():
    """
    Test that if `auto_updated_at=False`, `model_update()` should not update `updated_at`,
    even if the model has that field. Also verifies that `timezone.now()` is not called.
    """  # noqa: E501
    instance = TimestampsOpinionated()
    instance.full_clean()
    instance.save()

    data = {"created_at": timezone.now() - timedelta(days=1)}

    with patch("rolt.common.services.timezone.now") as now:
        updated_instance, has_updated = model_update(
            instance=instance,
            fields=["created_at"],
            data=data,
            auto_updated_at=False,
        )
        now.assert_not_called()

    assert has_updated is True
    assert updated_instance.updated_at is None


@pytest.mark.django_db
def test_if_model_update_skips_updated_at_if_model_does_not_have_it():
    """
    Test that if the model does not define an `updated_at` field,
    `model_update()` should skip setting it without any error.
    """
    instance = SimpleModelFactory()
    assert not hasattr(instance, "updated_at")

    with patch("rolt.common.services.timezone.now") as now:
        updated_instance, has_updated = model_update(
            instance=instance,
            fields=["name"],
            data={"name": "HackSoft"},
        )
        now.assert_not_called()

    assert has_updated is True
    assert not hasattr(updated_instance, "updated_at")
