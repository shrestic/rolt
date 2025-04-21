import uuid

from rolt.accounts.models.customer_model import Customer
from rolt.builds.models import Build


def build_exists(
    *,
    kit,
    switch,
    keycap,
    switch_quantity: int,
    customer=None,
) -> bool:
    """
    Check if a build with the given component combination already exists.

    - If `customer` is None → check among preset builds (is_preset=True).
    - If `customer` is not None → check among customer builds for that customer.
    """
    filters = {
        "kit": kit,
        "switch": switch,
        "keycap": keycap,
        "switch_quantity": switch_quantity,
    }

    if customer:
        filters["customer"] = customer
        filters["is_preset"] = False
    else:
        filters["customer__isnull"] = True
        filters["is_preset"] = True

    return Build.objects.filter(**filters).exists()


# Returns all builds of a specific customer.
def customer_build_list(*, customer) -> list[Build]:
    return (
        Build.objects.select_related("kit", "switch", "keycap", "customer")
        .filter(customer=customer, is_preset=False)
        .order_by("-created_at")
    )


# Returns all builds that are marked as presets.
def preset_builds_list() -> list[Build]:
    return (
        Build.objects.select_related("kit", "switch", "keycap")
        .filter(is_preset=True)
        .order_by("-created_at")
    )


def build_get_by_id(*, id: uuid.UUID) -> Build | None:  # noqa: A002
    return (
        Build.objects.select_related("kit", "switch", "keycap", "customer")
        .filter(id=id)
        .first()
    )


def customer_build_get_by_id(
    *,
    build_id: uuid.UUID,
    customer: Customer,
) -> Build | None:
    return (
        Build.objects.filter(id=build_id, customer=customer)
        .select_related("kit", "switch", "keycap", "customer")
        .first()
    )


def preset_build_get_by_id(*, build_id: uuid.UUID) -> Build | None:
    return (
        Build.objects.filter(customer__isnull=True, id=build_id)
        .select_related("kit", "switch", "keycap")
        .first()
    )


def build_check_duplicate_combo(
    *,
    kit,
    switch,
    keycap,
    exclude_build_id=None,
    customer=None,  # None if preset
) -> bool:
    """
    Check if the kit-switch-keycap combination already exists (excluding the current build).
    If a matching combo exists and it's not the current build → return True
    """  # noqa: E501

    qs = Build.objects.filter(
        kit=kit,
        switch=switch,
        keycap=keycap,
    )

    if exclude_build_id:
        qs = qs.exclude(id=exclude_build_id)

    qs = qs.filter(customer=customer) if customer else qs.filter(customer__isnull=True)

    return qs.exists()
