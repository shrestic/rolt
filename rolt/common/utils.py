import json
from functools import wraps
from hashlib import sha256

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
from faker import Faker
from rest_framework import serializers

faker = Faker()


def make_mock_object(**kwargs):
    return type("", (object,), kwargs)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        msg = f"{error_message_prefix} Could not find: {stringified_not_present}"
        raise ImproperlyConfigured(msg)

    return values


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def user_in_group(user, group_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


def clear_cache(
    *,
    prefix: str | None = None,
    filters: dict | None = None,
    specific_key: str | None = None,
) -> None:
    """
    Clear cache for keys matching a prefix, specific key, or generated from filters.

    Args:
        prefix: Cache key prefix (e.g., 'keycap_list:', 'kit_list:'). Clears all keys matching this prefix.
        filters: Dictionary of filters to generate a hashed key (used for keycap_list, kit_list, switch_list).
        specific_key: Exact cache key to clear (e.g., 'preset_builds_list').
    """  # noqa: E501
    try:
        if specific_key:
            # Delete a specific key (e.g., preset_builds_list)
            cache.delete(specific_key)

        if prefix and filters:
            # Generate a cache key using the prefix and filters (for keycap_list, kit_list, switch_list)  # noqa: E501
            filters_str = json.dumps(filters or {}, sort_keys=True)
            cache_key = f"{prefix}{sha256(filters_str.encode()).hexdigest()}"
            cache.delete(cache_key)

        elif prefix:
            # Delete all keys matching the prefix (e.g., keycap_list:*)
            keys = cache.keys(f"{prefix}*")
            if keys:
                cache.delete_many(keys)

    except AttributeError:
        pass


def invalidate_cache(prefix: str | None = None, specific_key: str | None = None):
    """
    Decorator to invalidate cache after a function execution.

    Args:
        prefix: Cache key prefix to clear (e.g., 'keycap_list:', 'kit_list:').
        specific_key: Specific cache key to clear (e.g., 'preset_builds_list').

    Usage:
        @invalidate_cache(prefix="keycap_list:")
        def update_keycap(...):
            ...

        @invalidate_cache(specific_key="preset_builds_list")
        def update_preset_build(...):
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            clear_cache(prefix=prefix, specific_key=specific_key)
            return result

        return wrapper

    return decorator
