import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rolt.accessories.models import Accessory
from rolt.builds.models import Build
from rolt.components.models.artisan_keycap_model import ArtisanKeycap
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch
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

    # Calculate the total reserved quantity
    reserved = query.aggregate(total=Sum("quantity"))["total"] or 0

    logger.debug(
        "Reserved quantity for product %s (ID: %s): %s units",
        product.__class__.__name__,
        product.id,
        reserved,
    )
    return reserved


def get_inventory(product):
    """
    Retrieve the inventory record for a product.

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
        # Retrieve the inventory record for the product
        inventory = inventory_model.objects.get(**{model_name: product})
    except inventory_model.DoesNotExist:
        error_msg = f"No inventory found for {model_name} (ID: {product.id})"
        logger.warning(error_msg)
        raise ValidationError(error_msg)  # noqa: B904

    logger.debug(
        "Inventory for %s (ID: %s): %s units",
        model_name,
        product.id,
        inventory.quantity,
    )
    return inventory


@receiver(post_save, sender=Accessory)
@receiver(post_save, sender=Keycap)
@receiver(post_save, sender=ArtisanKeycap)
@receiver(post_save, sender=Kit)
@receiver(post_save, sender=Switch)
def create_inventory(sender, instance, created, **kwargs):
    """
    Automatically create an inventory record when a product is created.

    Args:
        sender: The model class (e.g., Keycap, Kit).
        instance: The product instance being saved.
        created: Boolean indicating if the instance was just created.
        kwargs: Additional signal arguments.
    """
    if created:
        # Map product model names to their inventory models
        inventory_map = {
            "keycap": KeycapInventory,
            "artisankeycap": ArtisanKeycapInventory,
            "kit": KitInventory,
            "switch": SwitchInventory,
            "accessory": AccessoryInventory,
        }

        model_name = sender.__name__.lower()
        inventory_model = inventory_map[model_name]

        # Create or get the inventory record with initial quantity of 0
        inventory, created = inventory_model.objects.get_or_create(
            **{
                model_name: instance,
                "defaults": {"quantity": 0},
            },
        )

        logger.info(
            "Created inventory for %s (ID: %s, Created: %s)",
            model_name,
            instance.id,
            created,
        )


@receiver(post_delete, sender=Accessory)
@receiver(post_delete, sender=Keycap)
@receiver(post_save, sender=ArtisanKeycap)
@receiver(post_delete, sender=Kit)
@receiver(post_delete, sender=Switch)
def delete_inventory(sender, instance, **kwargs):
    """
    Automatically delete the inventory record when a product is deleted.

    Args:
        sender: The model class (e.g., Keycap, Kit).
        instance: The product instance being deleted.
        kwargs: Additional signal arguments.
    """
    # Map product model names to their inventory models
    inventory_map = {
        "keycap": KeycapInventory,
        "artisankeycap": ArtisanKeycapInventory,
        "kit": KitInventory,
        "switch": SwitchInventory,
        "accessory": AccessoryInventory,
    }

    model_name = sender.__name__.lower()
    inventory_model = inventory_map[model_name]

    # Delete the inventory record for the product
    deleted_count, _ = inventory_model.objects.filter(**{model_name: instance}).delete()

    logger.info(
        "Deleted %d inventory record(s) for %s (ID: %s)",
        deleted_count,
        model_name,
        instance.id,
    )


@receiver(pre_save, sender=Build)
def check_build_inventory(sender, instance, **kwargs):
    """
    Validate inventory for a Build instance before saving.

    Ensures sufficient stock exists for the Build's Kit, Switch, and Keycap,
    and that the switch quantity meets the kit's key requirements.

    Args:
        sender: The Build model class.
        instance: The Build instance being saved.
        kwargs: Additional signal arguments.

    Raises:
        ValidationError: If inventory is insufficient or switch quantity is too low.
    """
    logger.debug(
        "Checking inventory for Build (ID: %s)",
        instance.id if instance.id else "new",
    )

    # --- Check Kit Inventory ---
    kit = instance.kit
    kit_inventory = get_inventory(kit)
    kit_reserved = get_reserved_quantity(kit)
    kit_available = kit_inventory.quantity - kit_reserved
    if kit_available < 1:
        error_msg = f"Not enough stock for kit '{kit.name}'. Remaining: {kit_available}"
        logger.warning(error_msg)
        raise ValidationError(error_msg)

    # --- Check Switch Inventory ---
    switch = instance.switch
    switch_inventory = get_inventory(switch)
    switch_reserved = get_reserved_quantity(switch)
    switch_available = switch_inventory.quantity - switch_reserved
    if switch_available < instance.kit.number_of_keys:
        error_msg = f"Not enough stock for switch '{switch.name}'. Remaining: {switch_available}"  # noqa: E501
        logger.warning(error_msg)
        raise ValidationError(error_msg)

    # --- Check Keycap Inventory ---
    keycap = instance.keycap
    keycap_inventory = get_inventory(keycap)
    keycap_reserved = get_reserved_quantity(keycap)
    keycap_available = keycap_inventory.quantity - keycap_reserved
    if keycap_available < 1:
        error_msg = f"Not enough stock for keycap '{keycap.name}'. Remaining: {keycap_available}"  # noqa: E501
        logger.warning(error_msg)
        raise ValidationError(error_msg)

    logger.info(
        "Inventory check passed for Build (Kit: %s, Switch: %s, Keycap: %s)",
        kit.name,
        switch.name,
        keycap.name,
    )
