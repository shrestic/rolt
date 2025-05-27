from django.contrib import admin
from django.utils.html import format_html

from rolt.components.models.artisan_keycap_model import ArtisanKeycap
from rolt.components.models.keycap_model import Keycap
from rolt.components.models.kit_model import Kit
from rolt.components.models.switch_model import Switch


def format_currency(value):
    return f"{int(value):,} VND".replace(",", ".")


class ImagePreviewMixin:
    @admin.display(description="Image")
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Keycap)
class KeycapAdmin(admin.ModelAdmin, ImagePreviewMixin):
    autocomplete_fields = ("manufacturer",)
    list_display = (
        "name",
        "code",
        "manufacturer",
        "profile",
        "material",
        "formatted_price",
        "preview_image",
    )
    search_fields = ("name", "code", "colorway", "theme_name")
    list_filter = ("manufacturer", "profile", "material", "shine_through")
    readonly_fields = ("preview_image",)
    list_select_related = ("manufacturer",)

    @admin.display(description="Price (VND)")
    def formatted_price(self, obj):
        return format_currency(obj.price)


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin, ImagePreviewMixin):
    autocomplete_fields = ("manufacturer",)
    list_display = (
        "name",
        "code",
        "manufacturer",
        "type",
        "actuation_force",
        "bottom_out_force",
        "formatted_price_per_switch",
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
    list_select_related = ("manufacturer",)

    @admin.display(description="Price/Switch (VND)")
    def formatted_price_per_switch(self, obj):
        return format_currency(obj.price_per_switch)


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin, ImagePreviewMixin):
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
        "formatted_price",
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
    list_select_related = ("manufacturer",)

    @admin.display(description="Price (VND)")
    def formatted_price(self, obj):
        return format_currency(obj.price)


@admin.register(ArtisanKeycap)
class ArtisanKeycapAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "artist_name",
        "profile",
        "colorway",
        "formatted_price",
        "limited_quantity",
        "preview_image",
    )
    search_fields = ("name", "artist_name", "code")
    list_filter = ("profile", "colorway")
    ordering = ("-created_at",)
    readonly_fields = ("preview_image",)

    @admin.display(description="Price (VND)")
    def formatted_price(self, obj):
        return f"{int(obj.price):,} VND".replace(",", ".")

    @admin.display(description="Image")
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"
