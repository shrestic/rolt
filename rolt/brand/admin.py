# Register your models here.
from django.contrib import admin
from django.utils.html import format_html

from rolt.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "label",
        "logo_preview",
    )
    search_fields = (
        "code",
        "label",
    )
    ordering = ("code",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "logo_preview",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "label",
                    "logo",
                    "logo_preview",
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

    @admin.display(
        description="Preview",
    )
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="100" style="object-fit: contain; border: 1px solid #ddd;" />',  # noqa: E501
                obj.logo.url,
            )
        return "-"
