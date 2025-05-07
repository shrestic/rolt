from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from rolt.inventory.models import AccessoryInventory
from rolt.inventory.models import KeycapInventory
from rolt.inventory.models import KitInventory
from rolt.inventory.models import SwitchInventory


# === Shared base admin ===
class BaseInventoryAdmin(admin.ModelAdmin):
    """
    Shared logic for all inventory admin:
    - Filter dropdown when adding (only show unused products)
    - Make FK readonly when editing
    - Merge quantity if record already exists
    """

    model_field = None  # "kit", "keycap", ...
    object_name = None  # "kitinventory", ...
    fields = ()  # override in subclass
    search_fields = ()  # override in subclass
    ordering = ()  # override in subclass

    list_display = ("get_product_name", "quantity", "updated_at")
    list_filter = ("quantity",)
    readonly_fields = ("id", "updated_at")

    @admin.display(
        description="Product",
    )
    def get_product_name(self, obj):
        return getattr(obj, self.model_field).name

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (self.model_field,)  # noqa: RUF005
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == self.model_field and not request.resolver_match.kwargs.get(
            "object_id",
        ):
            model = db_field.related_model
            existing_ids = self.model.objects.values_list(
                f"{self.model_field}_id",
                flat=True,
            )
            kwargs["queryset"] = model.objects.exclude(id__in=existing_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        filter_kwargs = {self.model_field: getattr(obj, self.model_field)}
        existing = self.model.objects.filter(**filter_kwargs).first()

        if existing and not change:
            existing.quantity += obj.quantity
            existing.save()
            url = reverse(
                f"admin:inventory_{self.object_name}_change",
                args=(existing.id,),
            )
        else:
            obj.save()
            url = reverse(f"admin:inventory_{self.object_name}_change", args=(obj.id,))
        return HttpResponseRedirect(url)


# === Kit ===
@admin.register(KitInventory)
class KitInventoryAdmin(BaseInventoryAdmin):
    model = KitInventory
    model_field = "kit"
    object_name = "kitinventory"
    search_fields = ("kit__name",)
    ordering = ("kit__name",)
    fields = ("id", "kit", "quantity", "updated_at")


# === Keycap ===
@admin.register(KeycapInventory)
class KeycapInventoryAdmin(BaseInventoryAdmin):
    model = KeycapInventory
    model_field = "keycap"
    object_name = "keycapinventory"
    search_fields = ("keycap__name",)
    ordering = ("keycap__name",)
    fields = ("id", "keycap", "quantity", "updated_at")


# === Switch ===
@admin.register(SwitchInventory)
class SwitchInventoryAdmin(BaseInventoryAdmin):
    model = SwitchInventory
    model_field = "switch"
    object_name = "switchinventory"
    search_fields = ("switch__name",)
    ordering = ("switch__name",)
    fields = ("id", "switch", "quantity", "updated_at")


# === Accessory ===
@admin.register(AccessoryInventory)
class AccessoryInventoryAdmin(BaseInventoryAdmin):
    model = AccessoryInventory
    model_field = "accessory"
    object_name = "accessoryinventory"
    search_fields = ("accessory__name",)
    ordering = ("accessory__name",)
    fields = ("id", "accessory", "quantity", "updated_at")
