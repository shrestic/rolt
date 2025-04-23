from django.contrib import admin
from django.utils.html import format_html

from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


@admin.register(Keycap)
class KeycapAdmin(admin.ModelAdmin):
    autocomplete_fields = ("manufacturer",)
    list_display = (
        "name",
        "code",
        "manufacturer",
        "profile",
        "material",
        "price",
        "preview_image",
    )
    search_fields = ("name", "code", "colorway", "theme_name")
    list_filter = ("manufacturer", "profile", "material", "shine_through")
    readonly_fields = ("preview_image",)

    @admin.display(
        description="Image",
    )
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    autocomplete_fields = ("manufacturer",)
    list_display = (
        "name",
        "code",
        "manufacturer",
        "type",
        "actuation_force",
        "bottom_out_force",
        "price_per_switch",
        "preview_image",
    )
    search_fields = ("name", "code", "sound_level", "stem_material", "housing_material")
    list_filter = (
        "manufacturer",
        "type",
        "sound_level",
        "factory_lubed",
        "led_support",
        "pin_type",
    )
    readonly_fields = ("preview_image",)

    @admin.display(
        description="Image",
    )
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    autocomplete_fields = ("manufacturer",)
    list_display = (
        "name",
        "code",
        "manufacturer",
        "layout",
        "number_of_keys",
        "plate_material",
        "stab_mount",
        "hot_swap",
        "price",
        "preview_image",
    )
    search_fields = (
        "name",
        "code",
        "layout",
        "case_spec",
        "mounting_style",
        "firmware_type",
    )
    list_filter = (
        "manufacturer",
        "layout",
        "mounting_style",
        "plate_material",
        "hot_swap",
        "knob",
    )
    readonly_fields = ("preview_image",)

    @admin.display(
        description="Image",
    )
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"
