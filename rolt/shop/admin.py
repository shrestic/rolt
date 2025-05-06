from django.contrib import admin

from rolt.shop.models.cart_model import CartItem
from rolt.shop.models.order_model import Order
from rolt.shop.models.order_model import OrderItem
from rolt.shop.models.payment_transaction_model import PaymentTransaction


def is_product_manager(request):
    return request.user.groups.filter(name="Product Manager").exists()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "product_display", "quantity", "added_at")
    list_select_related = ("customer", "content_type")

    def get_fields(self, request, obj=None):
        return (
            "customer",
            "content_type",
            "object_id",
            "quantity",
            "added_at",
        )

    @admin.display(
        description="Product",
    )
    def product_display(self, obj):
        return f"{obj.content_type.model.capitalize()} | {obj.product}"

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product_display", "name_snapshot", "price_snapshot", "quantity")
    fields = ("product_display", "name_snapshot", "price_snapshot", "quantity")
    extra = 0

    @admin.display(
        description="Product",
    )
    def product_display(self, obj):
        return str(obj.product)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total_amount", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "customer__user__email")
    inlines = [OrderItemInline]
    list_select_related = ("customer__user",)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return ("customer", "total_amount", "created_at", "updated_at")

    def get_fields(self, request, obj=None):
        return ("customer", "status", "total_amount", "created_at")

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return is_product_manager(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "txn_ref",
        "order",
        "method",
        "status",
        "amount",
        "paid_at",
        "created_at",
    )
    list_filter = ("status", "method", "bank_code")
    search_fields = ("txn_ref", "order__id", "transaction_no", "bank_code")
    readonly_fields = (
        "txn_ref",
        "order",
        "method",
        "status",
        "amount",
        "bank_code",
        "transaction_no",
        "message",
        "paid_at",
        "created_at",
        "updated_at",
    )
    list_select_related = ("order",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True
