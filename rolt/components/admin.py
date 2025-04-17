from django.contrib import admin

from rolt.components.models.keycap_model import Keycap
from rolt.components.models.stabilizer_model import Stabilizer
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
        "description",
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


@admin.register(Stabilizer)
class StabilizerAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "label",
        "brand",
        "mount",
        "is_lubed",
        "price",
        "description",
    )
    list_filter = (
        "brand",
        "mount",
        "is_lubed",
    )
    search_fields = (
        "code",
        "label",
        "brand__label",
        "mount__label",
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
                    "mount",
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


@admin.register(Keycap)
class KeycapAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "label",
        "brand",
        "material",
        "profile",
        "theme",
        "price",
    )
    list_filter = (
        "brand",
        "material",
        "profile",
        "theme",
    )
    search_fields = (
        "code",
        "label",
        "brand__label",
        "material__label",
        "profile__label",
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
                    "material",
                    "profile",
                    "theme",
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
