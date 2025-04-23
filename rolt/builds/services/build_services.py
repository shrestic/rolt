from rolt.accounts.models.customer_model import Customer
from rolt.builds.cache import clear_preset_builds_cache
from rolt.builds.models import Build
from rolt.builds.models import SelectedService
from rolt.builds.models import Service
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


def calculate_total_price(
    kit: Kit,
    switch: Switch,
    switch_quantity: int,
    keycap: Keycap,
    extra_services: list[Service] | None,
):
    base_price = (
        (kit.price or 0)
        + (switch.price_per_switch or 0) * switch_quantity
        + (keycap.price or 0)
    )
    if extra_services:
        addon_price = sum(service.price for service in extra_services)
    else:
        addon_price = 0
    return base_price + addon_price


@clear_preset_builds_cache
def build_create(  # noqa: PLR0913
    *,
    name: str,
    kit: Kit,
    switch: Switch,
    keycap: Keycap,
    switch_quantity: int,
    customer: Customer | None,
    is_preset=False,
    selected_services: list[Service] | None,  # List[Service] or None
) -> Build:
    total_price = calculate_total_price(
        kit=kit,
        switch=switch,
        switch_quantity=switch_quantity,
        keycap=keycap,
        extra_services=selected_services if not is_preset else None,
    )

    build = Build.objects.create(
        name=name,
        kit=kit,
        switch=switch,
        keycap=keycap,
        switch_quantity=switch_quantity,
        total_price=total_price,
        customer=customer,
        is_preset=is_preset,
    )

    # Only attach services if not preset
    if not is_preset and selected_services:
        for service in selected_services:
            SelectedService.objects.create(
                build=build,
                service=service,
                price=service.price,
            )

    return build


@clear_preset_builds_cache
def build_update(  # noqa: PLR0913
    *,
    instance: Build,
    name: str | None,
    kit: Kit | None,
    switch: Switch | None,
    keycap: Keycap | None,
    switch_quantity: int | None,
    selected_services: list[Service] | None,
) -> Build:
    fields_to_update = []

    if name:
        instance.name = name
        fields_to_update.append("name")
    if kit:
        instance.kit = kit
        fields_to_update.append("kit")
    if switch:
        instance.switch = switch
        fields_to_update.append("switch")
    if keycap:
        instance.keycap = keycap
        fields_to_update.append("keycap")
    if switch_quantity is not None:
        instance.switch_quantity = switch_quantity
        fields_to_update.append("switch_quantity")

    # Update selected services if provided (for custom builds only)
    if not instance.is_preset and selected_services is not None:
        # Remove old
        SelectedService.objects.filter(build=instance).delete()
        # Add new
        for service in selected_services:
            SelectedService.objects.create(
                build=instance,
                service=service,
                price=service.price,
            )

    # Recalculate price
    extra_services = selected_services if not instance.is_preset else None
    instance.total_price = calculate_total_price(
        kit=instance.kit,
        switch=instance.switch,
        switch_quantity=instance.switch_quantity,
        keycap=instance.keycap,
        extra_services=extra_services,
    )
    fields_to_update.append("total_price")

    instance.save(update_fields=fields_to_update)
    return instance


@clear_preset_builds_cache
def build_delete(*, instance: Build) -> None:
    instance.delete()
