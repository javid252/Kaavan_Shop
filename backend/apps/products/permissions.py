from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """هرکسی می‌تواند بخواند؛ فقط ادمین (is_staff) می‌تواند تغییر دهد."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsAdminOrVendorOwner(permissions.BasePermission):
    """
    هرکسی می‌تواند بخواند. برای نوشتن: ادمین همیشه اجازه دارد؛ یک فروشنده
    تاییدشده فقط وقتی حالت چندفروشندگی روشن باشد اجازه دارد محصولات خودش
    را بسازد/ویرایش/حذف کند. اگر چندفروشندگی خاموش باشد، فقط ادمین می‌تواند
    بنویسد - دقیقاً مثل حالت تک‌فروشگاهی قبلی.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True

        from apps.vendors.permissions import multivendor_enabled  # جلوگیری از import چرخه‌ای

        if not multivendor_enabled():
            return False
        vendor = getattr(user, "vendor_profile", None)
        return bool(vendor and vendor.is_approved)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_staff:
            return True
        vendor = getattr(user, "vendor_profile", None)
        return bool(vendor and obj.vendor_id == vendor.id)