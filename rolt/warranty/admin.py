from django.contrib import admin

from rolt.warranty.models import Warranty
from rolt.warranty.models import WarrantyRequest


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderitem",
        "customer",
        "start_date",
        "end_date",
        "status",
        "short_notes",
    )
    list_filter = ("status", "start_date", "end_date")
    search_fields = (
        "id",
        "customer__user__email",
        "orderitem__name_snapshot",
        "notes",
    )
    readonly_fields = ("start_date", "end_date", "orderitem", "customer", "created_at")
    date_hierarchy = "start_date"
    list_select_related = ("orderitem", "customer__user")

    @admin.display(
        description="Notes",
    )
    def short_notes(self, obj):
        return (
            obj.notes[:50] + "..." if obj.notes and len(obj.notes) > 50 else obj.notes  # noqa: PLR2004
        )


@admin.register(WarrantyRequest)
class WarrantyRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "warranty",
        "customer",
        "status",
        "short_description",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "id",
        "warranty__id",
        "customer__user__email",
        "description",
        "admin_notes",
    )
    date_hierarchy = "created_at"
    list_select_related = ("warranty", "customer__user")
    readonly_fields = ("created_at", "warranty", "customer", "description")

    def has_delete_permission(self, request, obj=...):
        return False

    @admin.display(
        description="Description",
    )
    def short_description(self, obj):
        return (
            obj.description[:50] + "..."
            if obj.description and len(obj.description) > 50  # noqa: PLR2004
            else obj.description
        )
