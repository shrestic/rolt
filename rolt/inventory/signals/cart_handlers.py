import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rolt.inventory.models import AccessoryInventory
from rolt.inventory.models import ArtisanKeycapInventory
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.shop.models.cart_model import CartItem

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
        raise ValidationError(error_msg)  # noqa: B904

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


@receiver(pre_save, sender=CartItem)
@transaction.atomic
def validate_cart_item_inventory(sender, instance, **kwargs):
    """
    Validate that sufficient inventory exists before saving a CartItem.

    This signal runs before a CartItem is saved, ensuring:
    - For regular products (Keycap, Kit, Switch, Accessory), enough stock exists.
    - For Build products, enough stock exists for the associated Kit, Switch, and Keycap.

    Uses SELECT FOR UPDATE to lock inventory records and prevent race conditions.

    Note:
    This validation only checks actual inventory quantity.
    Reserved quantities in other carts are NOT considered here.
    Actual inventory deduction should happen during order placement.
    """  # noqa: E501
    product = instance.product
    product_name = str(product)
    quantity = instance.quantity

    logger.debug(
        "Checking inventory for CartItem (ID: %s, Product: %s, Quantity: %s)",
        instance.id or "new",
        product_name,
        quantity,
    )

    if product.__class__.__name__.lower() == "build":
        build = product

        total_builds = quantity
        total_switches_required = total_builds * build.kit.number_of_keys

        # --- Kit inventory check ---
        kit_inventory = lock_inventory(build.kit)
        kit_available = kit_inventory.quantity
        if kit_available < total_builds:
            handle_out_of_stock(build.kit.name, kit_available)

        # --- Switch inventory check ---
        switch_inventory = lock_inventory(build.switch)
        switch_available = switch_inventory.quantity
        if switch_available < total_switches_required:
            handle_out_of_stock(build.switch.name, switch_available)

        # --- Keycap inventory check ---
        keycap_inventory = lock_inventory(build.keycap)
        keycap_available = keycap_inventory.quantity
        if keycap_available < total_builds:
            handle_out_of_stock(build.keycap.name, keycap_available)

    else:
        inventory = lock_inventory(product)
        available = inventory.quantity
        if available < quantity:
            handle_out_of_stock(product_name, available)

    logger.info(
        "Inventory check passed for CartItem (Product: %s, Quantity: %s)",
        product_name,
        quantity,
    )
