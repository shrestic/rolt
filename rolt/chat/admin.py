from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html

from .models import Message
from .models import Room

User = get_user_model()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "content", "timestamp")
    list_filter = ("room", "user")
    search_fields = ("room__name", "user__email", "content")
    list_per_page = 20


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "customer",
        "assigned_to",
        "is_active",
        "view_messages_link",
    ]
    search_fields = ["name", "customer__email", "assigned_to__email"]
    readonly_fields = ["view_messages_link"]

    @admin.display(
        description="Messages",
    )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            # Filter only users in group 'support' or 'technician'
            support_users = User.objects.filter(
                groups__name__in=["Support", "Technician"],
            ).distinct()
            kwargs["queryset"] = support_users
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def view_messages_link(self, obj):
        if not obj.id:
            return "-"
        if not Message.objects.filter(room=obj).exists():
            return "No messages"
        url = reverse("admin:chat_message_changelist") + f"?room__id__exact={obj.id}"
        return format_html('<a href="{}" target="_blank">View messages</a>', url)
