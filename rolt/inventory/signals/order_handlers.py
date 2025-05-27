import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rolt.inventory.models import AccessoryInventory
from rolt.inventory.models import ArtisanKeycapInventory
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.shop.models.order_model import Order

logger = logging.getLogger(__name__)


def lock_inventory(product):
    """
    Retrieve and lock the inventory record for a product to prevent race conditions.

    Args:
        product: The product instance (e.g., Keycap, Kit, Switch, Accessory).

    Returns:
        Inventory model instance (e.g., KeycapInventory, KitInventory).

    Raises:
        ValidationError: If no inventory model exists or no record is found.
    """
    inventory_map = {
        "keycap": KeycapInventory,
        "artisankeycap": ArtisanKeycapInventory,
        "kit": KitInventory,
        "switch": SwitchInventory,
        "accessory": AccessoryInventory,
    }

    model_name = product.__class__.__name__.lower()

    if model_name not in inventory_map:
        error_msg = f"No inventory model defined for {model_name} (ID: {product.id})"
        logger.warning(error_msg)
        raise ValidationError(error_msg)

    inventory_model = inventory_map[model_name]

    try:
        # Lock the inventory record to prevent concurrent modifications
        inventory = inventory_model.objects.select_for_update().get(
            **{model_name: product},
        )
    except inventory_model.DoesNotExist:
        error_msg = f"No inventory found for {model_name} (ID: {product.id})"
        logger.warning(error_msg)
        raise ValidationError(error_msg) from None

    logger.debug(
        "Locked inventory for %s (ID: %s): %s units",
        model_name,
        product.id,
        inventory.quantity,
    )
    return inventory


def handle_out_of_stock(product_name, remaining):
    """
    Raise a ValidationError for out-of-stock situations with consistent logging.

    Args:
        product_name: Name of the product.
        remaining: Remaining quantity in inventory.

    Raises:
        ValidationError: Indicates insufficient stock.
    """
    error_msg = f"Not enough stock for {product_name}. Remaining: {remaining} units"
    logger.warning(error_msg)
    raise ValidationError(error_msg)


def process_build_inventory(build, quantity, operation="check"):
    """
    Process inventory for a build product (kit + switches + keycaps).

    Args:
        build: The build product instance.
        quantity: Number of builds to process.
        operation: Operation type - "check", "deduct", or "restore".

    Returns:
        None for check operations, True for successful updates.

    Raises:
        ValidationError: If insufficient inventory during check operations.
    """
    total_builds = quantity
    total_switches_required = total_builds * build.kit.number_of_keys

    components = [
        (build.kit, total_builds, "kit"),
        (build.switch, total_switches_required, "switch"),
        (build.keycap, total_builds, "keycap"),
    ]

    for component, required_quantity, component_type in components:
        inventory = lock_inventory(component)

        if operation == "check":
            available = inventory.quantity
            if available < required_quantity:
                handle_out_of_stock(component.name, available)

        elif operation == "deduct":
            inventory.quantity -= required_quantity
            inventory.save()
            logger.info(
                "Inventory updated for %s %s: %s units deducted",
                component_type,
                component.name,
                required_quantity,
            )

        elif operation == "restore":
            inventory.quantity += required_quantity
            inventory.save()
            logger.info(
                "Inventory restored for %s %s: %s units added",
                component_type,
                component.name,
                required_quantity,
            )


def process_regular_inventory(product, quantity, operation="check"):
    """
    Process inventory for regular (non-build) products.

    Args:
        product: The product instance.
        quantity: Quantity to process.
        operation: Operation type - "check", "deduct", or "restore".

    Returns:
        None for check operations, True for successful updates.

    Raises:
        ValidationError: If insufficient inventory during check operations.
    """
    inventory = lock_inventory(product)

    if operation == "check":
        available = inventory.quantity
        if available < quantity:
            handle_out_of_stock(str(product), available)

    elif operation == "deduct":
        inventory.quantity -= quantity
        inventory.save()
        logger.info(
            "Inventory updated for product %s: %s units deducted",
            product,
            quantity,
        )

    elif operation == "restore":
        inventory.quantity += quantity
        inventory.save()
        logger.info(
            "Inventory restored for product %s: %s units added",
            product,
            quantity,
        )


def process_order_inventory(order, operation="check"):
    """
    Process inventory for all items in an order.

    Args:
        order: The Order instance.
        operation: Operation type - "check", "deduct", or "restore".

    Raises:
        ValidationError: If insufficient inventory during check operations.
    """
    action_msg = {
        "check": "Checking",
        "deduct": "Updating",
        "restore": "Restoring",
    }

    logger.info("%s inventory for Order %s", action_msg[operation], order.id)

    for item in order.items.all():
        product = item.product
        quantity = item.quantity

        logger.debug(
            "%s inventory for product %s quantity %s",
            action_msg[operation],
            product,
            quantity,
        )

        is_build = product.__class__.__name__.lower() == "build"

        if is_build:
            process_build_inventory(product, quantity, operation)
        else:
            process_regular_inventory(product, quantity, operation)

    if operation == "check":
        logger.info("Inventory check passed for Order %s", order.id)
    else:
        logger.info("Inventory %s completed for Order %s", operation, order.id)


@receiver(post_save, sender=Order)
def restore_inventory_on_cancelled_order(sender, instance, created, **kwargs):
    """
    Restore inventory when an Order is cancelled.
    """
    if not created and instance.status == Order.StatusChoices.CANCELLED:
        logger.info("Order %s cancelled, restoring inventory", instance.id)

        with transaction.atomic():
            process_order_inventory(instance, operation="restore")


@receiver(pre_save, sender=Order)
def check_inventory_before_order_creation(sender, instance, **kwargs):
    """
    Check inventory before saving a new Order.
    """
    # Only check for new orders (created=True is not available in pre_save)
    if instance.pk is None:  # New instance
        process_order_inventory(instance, operation="check")


@receiver(post_save, sender=Order)
def update_inventory_on_order_paid(sender, instance, created, **kwargs):
    """
    Update inventory when an Order is paid.
    """
    if not created and instance.status == Order.StatusChoices.PAID:
        logger.info("Order %s paid, updating inventory", instance.id)

        with transaction.atomic():
            process_order_inventory(instance, operation="deduct")
