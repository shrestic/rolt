from django.contrib import admin

from rolt.components.models.switch_model import Switch


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "label",
        "brand",
        "type",
        "is_lubed",
        "price",
    )
    list_filter = (
        "brand",
        "type",
        "is_lubed",
    )
    search_fields = (
        "code",
        "label",
        "brand__label",
        "type__label",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("code",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "label",
                    "brand",
                    "type",
                    "is_lubed",
                    "price",
                    "image",
                    "description",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
