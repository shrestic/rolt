from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from rolt.common.models import RandomModel


@pytest.mark.django_db
def test_if_full_clean_raises_validation_error_if_constraint_fails():
    # Arrange
    start_date = timezone.now().date()
    end_date = start_date - timedelta(days=1)

    # Act & Assert
    with pytest.raises(ValidationError):  # noqa: PT012
        obj = RandomModel(start_date=start_date, end_date=end_date)
        obj.full_clean()
        obj.save()


@pytest.mark.django_db
def test_if_create_raises_integrity_error_if_constraint_fails():
    # Arrange
    start_date = timezone.now().date()
    end_date = start_date - timedelta(days=1)

    # Act & Assert
    with pytest.raises(IntegrityError):
        RandomModel.objects.create(start_date=start_date, end_date=end_date)


@pytest.mark.django_db
def test_if_create_succeeds_when_constraint_is_valid():
    # Arrange
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=1)

    # Assert initial state
    assert RandomModel.objects.count() == 0

    # Act
    RandomModel.objects.create(start_date=start_date, end_date=end_date)

    # Assert
    assert RandomModel.objects.count() == 1
