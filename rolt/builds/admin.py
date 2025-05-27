from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.html import format_html

from rolt.builds.models import Build
from rolt.builds.models import SelectedService
from rolt.builds.models import Service
from rolt.builds.models import Showcase


# Common formatter
def format_currency(value):
    return f"{int(value):,} VND".replace(",", ".")


# Image preview reusable
class ImagePreviewMixin:
    @admin.display(description="Image")
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border:1px solid #ccc;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    autocomplete_fields = ("customer", "kit", "switch", "keycap")
    list_display = (
        "name",
        "kit",
        "switch",
        "keycap",
        "formatted_total_price",
        "is_preset",
        "customer",
        "created_at",
    )
    list_filter = ("is_preset", "kit__layout", "switch__type", "keycap__profile")
    search_fields = (
        "name",
        "kit__name",
        "switch__name",
        "keycap__name",
        "customer__user__username",
    )
    ordering = ("-created_at",)
    list_select_related = (
        "kit",
        "switch",
        "keycap",
        "customer__user",
    )

    @admin.display(description="Total Price (VND)")
    def formatted_total_price(self, obj):
        return format_currency(obj.total_price)

    def has_change_permission(self, request, obj=None):
        if obj and not obj.is_preset:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.is_preset:
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_preset=True)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin, ImagePreviewMixin):
    list_display = ("name", "code", "formatted_price", "preview_image")
    search_fields = ("name", "code", "description")
    readonly_fields = ("preview_image",)

    @admin.display(description="Price (VND)")
    def formatted_price(self, obj):
        return format_currency(obj.price)


class SelectedServiceForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        build = cleaned_data.get("build")
        if build and not build.is_preset:
            msg = "Cannot assign services to non-preset builds!"
            raise ValidationError(msg)
        return cleaned_data


@admin.register(SelectedService)
class SelectedServiceAdmin(admin.ModelAdmin):
    form = SelectedServiceForm
    autocomplete_fields = ("build", "service")
    list_display = ("build", "service", "formatted_price")
    list_filter = ("service__name",)
    search_fields = ("build__name", "service__name")
    list_select_related = ("build", "service")

    @admin.display(description="Price (VND)")
    def formatted_price(self, obj):
        return format_currency(obj.price)


class ShowcaseForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        build = cleaned_data.get("build")
        if build and not build.is_preset:
            msg = "Only preset builds can have a showcase."
            raise ValidationError(msg)
        return cleaned_data


@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin, ImagePreviewMixin):
    form = ShowcaseForm
    autocomplete_fields = ("build",)
    list_display = ("title", "build", "preview_image", "created_at")
    search_fields = ("title", "description", "build__name")
    readonly_fields = ("preview_image",)
    ordering = ("-created_at",)
    list_select_related = ("build",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "build":
            from rolt.builds.models import Build

            kwargs["queryset"] = Build.objects.filter(is_preset=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
