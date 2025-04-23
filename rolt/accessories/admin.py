from django.contrib import admin
from django.utils.html import format_html

from rolt.accessories.models import Accessory


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "preview_image")
    search_fields = ("name", "type")
    list_filter = ("type",)
    ordering = ("name",)

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
