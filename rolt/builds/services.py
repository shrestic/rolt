from rolt.builds.models import Build


def build_delete(*, instance: Build) -> None:
    instance.delete()


def calculate_total_price(kit, switch, switch_quantity, keycap):
    return (
        (kit.price or 0)
        + (switch.price_per_switch or 0) * switch_quantity
        + (keycap.price or 0)
    )


def build_create(  # noqa: PLR0913
    *,
    name,
    kit,
    switch,
    keycap,
    switch_quantity,
    customer=None,
    is_preset=False,
) -> Build:
    total_price = calculate_total_price(
        kit=kit,
        switch=switch,
        switch_quantity=switch_quantity,
        keycap=keycap,
    )

    return Build.objects.create(
        name=name,
        kit=kit,
        switch=switch,
        keycap=keycap,
        switch_quantity=switch_quantity,
        total_price=total_price,
        customer=customer,
        is_preset=is_preset,
    )


def build_update(  # noqa: PLR0913
    *,
    instance: Build,
    name=None,
    kit=None,
    switch=None,
    keycap=None,
    switch_quantity=None,
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

    # Recalculate total_price
    instance.total_price = calculate_total_price(
        kit=instance.kit,
        switch=instance.switch,
        switch_quantity=instance.switch_quantity,
        keycap=instance.keycap,
    )
    fields_to_update.append("total_price")

    instance.save(update_fields=fields_to_update)
    return instance
