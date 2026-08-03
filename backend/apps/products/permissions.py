from rest_framework import permissions

from apps.access.permissions import model_perm_codename


class IsAdminOrReadOnly(permissions.BasePermission):
    """هرکسی می‌تواند بخواند؛ فقط ادمینِ دارای پرمیشن مربوطه می‌تواند تغییر دهد."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated and user.is_staff):
            return False
        queryset = getattr(view, "queryset", None)
        if queryset is None:
            return True
        codename = model_perm_codename(request.method, queryset.model._meta.app_label, queryset.model._meta.model_name)
        return not codename or user.has_perm(codename)


class IsAdminOrVendorOwner(permissions.BasePermission):
    """
    هرکسی می‌تواند بخواند. برای نوشتن: ادمینی که پرمیشن products مربوطه را
    داشته باشد (مثلاً «اپراتور ویرایش محصول») همیشه اجازه دارد؛ یک فروشنده
    تاییدشده فقط وقتی حالت چندفروشندگی روشن باشد اجازه دارد محصولات خودش
    را بسازد/ویرایش/حذف کند. اگر چندفروشندگی خاموش باشد، فقط staff دارای
    پرمیشن می‌تواند بنویسد - دقیقاً مثل حالت تک‌فروشگاهی قبلی.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            codename = model_perm_codename(request.method, "products", "product")
            return not codename or user.has_perm(codename)

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
            codename = model_perm_codename(request.method, "products", "product")
            return not codename or user.has_perm(codename)
        vendor = getattr(user, "vendor_profile", None)
        return bool(vendor and obj.vendor_id == vendor.id)


class CanManageProductRelated(permissions.BasePermission):
    """
    برای ProductImage و ProductVariant: ادمینِ دارای پرمیشن، یا فروشنده‌ای که
    مالک محصولِ مربوطه است. قبلاً این دو ViewSet کلاً admin-only بودند که یعنی
    فروشنده‌ها اصلاً نمی‌توانستند برای محصول خودشان عکس/تنوع اضافه کنند - این
    نسخه آن مشکل را هم رفع می‌کند.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            codename = model_perm_codename(request.method, "products", "product")
            return not codename or user.has_perm(codename)

        vendor = getattr(user, "vendor_profile", None)
        if not (vendor and vendor.is_approved):
            return False
        if request.method == "POST":
            from .models import Product

            product_id = request.data.get("product")
            return bool(product_id) and Product.objects.filter(pk=product_id, vendor=vendor).exists()
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            codename = model_perm_codename(request.method, "products", "product")
            return not codename or user.has_perm(codename)
        vendor = getattr(user, "vendor_profile", None)
        return bool(vendor and obj.product.vendor_id == vendor.id)