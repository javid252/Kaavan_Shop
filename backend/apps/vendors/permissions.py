from rest_framework import permissions

from .models import PlatformSettings


class IsApprovedVendor(permissions.BasePermission):
    """کاربر باید یک پروفایل فروشنده تاییدشده داشته باشد."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        vendor = getattr(request.user, "vendor_profile", None)
        return bool(vendor and vendor.is_approved)


def multivendor_enabled():
    return PlatformSettings.load().multivendor_enabled