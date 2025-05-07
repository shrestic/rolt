import logging

from django.db.models import F

from rolt.inventory.models import AccessoryInventory
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory
from rolt.shop.models.payment_transaction_model import PaymentTransaction

logger = logging.getLogger(__name__)


def _update_inventory(product, quantity_change: int):
    """
    Update the inventory quantity for a product by the specified amount.

    Args:
        product: The product instance (e.g., Keycap, Kit, Switch, Accessory).
        quantity_change: The amount to add (positive) or subtract (negative) from inventory.

    Returns:
        Inventory model instance (e.g., KeycapInventory, KitInventory) after update.

    Raises:
        Inventory model DoesNotExist: If no inventory record is found for the product.
    """  # noqa: E501
    # Map product model names to their inventory models
    inventory_map = {
        "keycap": KeycapInventory,
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
        raise ValueError(error_msg)

    # Get the inventory model (e.g., KeycapInventory)
    inventory_model = inventory_map[model_name]

    # Lock and update the inventory record using SELECT FOR UPDATE
    inventory = inventory_model.objects.select_for_update().get(**{model_name: product})
    inventory.quantity = F("quantity") + quantity_change
    inventory.save()

    logger.debug(
        "Updated inventory for %s (ID: %s) by %s units",
        model_name,
        product.id,
        quantity_change,
    )
    return inventory


def process_payment_inventory_change(
    payment_transaction: PaymentTransaction,
    old_status: str,
):
    """
    Update inventory based on payment transaction status changes.

    - Deducts inventory for successful payments (status changes to SUCCESS).
    - Restores inventory for failed or canceled payments after a successful payment.
    - Skips updates if the status hasn't changed or for unhandled transitions.
    """
    logger.warning(
        "[PAYMENT PROCESSING] Payment %s - status=%s - old_status=%s",
        payment_transaction.txn_ref,
        payment_transaction.status,
        old_status,
    )

    if payment_transaction.status == old_status:
        logger.debug("No status change; skipping inventory update.")
        return

    # Handle payment success → deduct inventory
    if (
        payment_transaction.status == PaymentTransaction.StatusChoices.SUCCESS
        and old_status != PaymentTransaction.StatusChoices.SUCCESS
    ):
        logger.info(
            "[PAYMENT SUCCESS] Deducting inventory for order %s",
            payment_transaction.order_id,
        )

        for item in payment_transaction.order.items.all():
            product = item.product
            quantity = item.quantity
            logger.debug("Processing item: %s x%s", product, quantity)

            if product.__class__.__name__.lower() == "build":
                _update_inventory(product.kit, -quantity)
                _update_inventory(
                    product.switch,
                    -quantity * product.kit.number_of_keys,
                )
                _update_inventory(product.keycap, -quantity)
            else:
                _update_inventory(product, -quantity)

            logger.info("Inventory deducted for %s", product)

    # Handle cancel/fail → restore inventory
    elif (
        payment_transaction.status
        in [
            PaymentTransaction.StatusChoices.FAILED,
            PaymentTransaction.StatusChoices.CANCELLED,
        ]
        and old_status == PaymentTransaction.StatusChoices.SUCCESS
    ):
        logger.info(
            "[PAYMENT RESTORE] Restoring inventory for order %s",
            payment_transaction.order_id,
        )

        for item in payment_transaction.order.items.all():
            product = item.product
            quantity = item.quantity
            logger.debug("Restoring item: %s x%s", product, quantity)

            if product.__class__.__name__.lower() == "build":
                _update_inventory(product.kit, quantity)
                _update_inventory(product.switch, quantity * product.kit.number_of_keys)
                _update_inventory(product.keycap, quantity)
            else:
                _update_inventory(product, quantity)

            logger.info("Inventory restored for %s", product)

    else:
        logger.debug(
            "Unhandled status transition: %s → %s",
            old_status,
            payment_transaction.status,
        )
