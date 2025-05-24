import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rolt.inventory.models import AccessoryInventory
from rolt.inventory.models import ArtisanKeycapInventory
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.shop.models.cart_model import CartItem

logger = logging.getLogger(__name__)


def get_reserved_quantity(product, exclude_cart_item_id=None):
    """
    Calculate the total quantity of a product reserved in other cart items.

    Args:
        product: The product instance (e.g., Keycap, Kit, Switch, Accessory).
        exclude_cart_item_id: Optional ID of a CartItem to exclude.

    Returns:
        int: Total quantity reserved by other cart items.
    """
    # Get the ContentType for the product model
    content_type = ContentType.objects.get_for_model(product)

    # Query to get all CartItems with the same product type and ID
    query = CartItem.objects.filter(
        content_type=content_type,
        object_id=product.id,
    )

    # If exclude_cart_item_id is provided, exclude it from the query
    if exclude_cart_item_id:
        query = query.exclude(id=exclude_cart_item_id)

    # Calculate the total reserved quantity
    reserved = query.aggregate(total=Sum("quantity"))["total"] or 0

    logger.debug(
        "Reserved quantity for product %s (ID: %s): %s units",
        product.__class__.__name__,
        product.id,
        reserved,
    )
    return reserved


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
    # Map product model names to their inventory models
    inventory_map = {
        "keycap": KeycapInventory,
        "artisankeycap": ArtisanKeycapInventory,
        "kit": KitInventory,
        "switch": SwitchInventory,
        "accessory": AccessoryInventory,
    }

    # Get the model name (e.g., 'keycap', 'kit')
    model_name = product.__class__.__name__.lower()

    # Check if an inventory model exists for this product type
    if model_name not in inventory_map:
        error_msg = f"No inventory model defined for {model_name} (ID: {product.id})"
        logger.warning(error_msg)
        raise ValidationError(error_msg)

    # Get the inventory model (e.g., KeycapInventory)
    inventory_model = inventory_map[model_name]

    try:
        # Lock the inventory record using SELECT FOR UPDATE to prevent concurrent modifications  # noqa: E501
        inventory = inventory_model.objects.select_for_update().get(
            **{model_name: product},
        )
    except inventory_model.DoesNotExist:
        error_msg = f"No inventory found for {model_name} (ID: {product.id})"
        logger.warning(error_msg)
        raise ValidationError(error_msg)  # noqa: B904

    # Log the inventory details
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
        remaining: Remaining quantity in inventory after reservations.

    Raises:
        ValidationError: With a message indicating insufficient stock.
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

        # --- Kit ---
        kit_inventory = lock_inventory(build.kit)
        kit_reserved = get_reserved_quantity(build.kit, instance.id)
        kit_available = kit_inventory.quantity - kit_reserved
        if kit_available < total_builds:
            handle_out_of_stock(build.kit.name, kit_available)

        # --- Switch ---
        switch_inventory = lock_inventory(build.switch)
        switch_reserved = get_reserved_quantity(build.switch, instance.id)
        switch_available = switch_inventory.quantity - switch_reserved
        if switch_available < total_switches_required:
            handle_out_of_stock(build.switch.name, switch_available)

        # --- Keycap ---
        keycap_inventory = lock_inventory(build.keycap)
        keycap_reserved = get_reserved_quantity(build.keycap, instance.id)
        keycap_available = keycap_inventory.quantity - keycap_reserved
        if keycap_available < total_builds:
            handle_out_of_stock(build.keycap.name, keycap_available)

    else:
        inventory = lock_inventory(product)
        reserved = get_reserved_quantity(product, instance.id)
        available = inventory.quantity - reserved
        if available < quantity:
            handle_out_of_stock(product_name, available)

    logger.info(
        "Inventory check passed for CartItem (Product: %s, Quantity: %s)",
        product_name,
        quantity,
    )
