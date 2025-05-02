from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Room

User = get_user_model()


@admin.register(Room)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["name", "customer", "assigned_to", "is_active"]
    search_fields = ["name", "customer__email", "assigned_to__email"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            # Filter only users in group 'support' or 'technician'
            support_users = User.objects.filter(
                groups__name__in=["Support", "Technician"],
            ).distinct()
            kwargs["queryset"] = support_users
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
