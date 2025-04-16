from rest_framework.permissions import BasePermission

from rolt.common.utils import user_in_group


class IsSupportStaff(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Support")


class IsProductManager(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Product Manager")


class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Technician")


class IsDesigner(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Content Designer")


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Customer")


class IsFinanceTeam(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Finance")


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsInAllowedGroups(BasePermission):
    """
    Check if the user is in one of the allowed groups.
    """

    allowed_groups = []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and any(user_in_group(request.user, group) for group in self.allowed_groups)
        )


class IsSupportOrProductManager(IsInAllowedGroups):
    allowed_groups = ["Support", "Product Manager"]


class IsCustomerOrTechnician(IsInAllowedGroups):
    allowed_groups = ["Customer", "Technician"]
