import uuid

from django.db.models import QuerySet

from rolt.accounts.models.customer_model import Customer
from rolt.builds.models import Build
from rolt.builds.models import Service
from rolt.builds.models import Showcase
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


def build_exists(
    *,
    kit: Kit,
    switch: Switch,
    keycap: Keycap,
    switch_quantity: int,
    customer: Customer | None,
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
        .prefetch_related("selected_services__service")
        .filter(customer=customer, is_preset=False)
        .order_by("-created_at")
    )


# Returns all builds that are marked as presets.
def preset_builds_list() -> list[Build]:
    return (
        Build.objects.select_related("kit", "switch", "keycap")
        .prefetch_related("selected_services__service")
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
    id: uuid.UUID,  # noqa: A002
    customer: Customer,
) -> Build | None:
    return (
        Build.objects.filter(id=id, customer=customer)
        .select_related("kit", "switch", "keycap", "customer")
        .first()
    )


def preset_build_get_by_id(*, id: uuid.UUID) -> Build | None:  # noqa: A002
    return (
        Build.objects.filter(customer__isnull=True, id=id)
        .select_related("kit", "switch", "keycap")
        .first()
    )


def build_check_duplicate_combo(
    *,
    kit: Kit,
    switch: Switch,
    keycap: Keycap,
    exclude_build_id=None,
    customer: Customer | None,  # None if preset
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


def showcase_list() -> QuerySet[Showcase]:
    return (
        Showcase.objects.select_related("build")
        .filter(build__is_preset=True)
        .order_by("-build__created_at")
    )


def showcase_get(
    *,
    id: uuid.UUID,  # noqa: A002
) -> Showcase | None:
    return Showcase.objects.select_related("build").filter(id=id).first()


def showcase_get_by_build_id(
    *,
    build_id: uuid.UUID,
) -> Showcase | None:
    return Showcase.objects.select_related("build").filter(build_id=build_id).first()


def service_list_by_codes(
    *,
    codes: list[str],
) -> QuerySet[Service]:
    return Service.objects.filter(code__in=codes)


def service_list() -> list[Service]:
    return list(Service.objects.all())


def service_get_by_code(
    *,
    code: str,
) -> Service | None:
    return Service.objects.filter(code=code).first()
