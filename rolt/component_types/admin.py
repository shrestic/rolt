from django.contrib import admin

from rolt.component_types.models import ComponentType


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "applies_to", "note", "created_at", "updated_at")
    list_filter = ("applies_to",)
    search_fields = ("code", "label")
    ordering = ("code",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("code", "label", "applies_to", "note")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
