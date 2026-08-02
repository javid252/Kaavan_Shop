from rest_framework import serializers

from .models import PlatformSettings, Vendor


class PlatformSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSettings
        fields = ["multivendor_enabled", "default_commission_percent"]


class PublicSettingsSerializer(serializers.ModelSerializer):
    """نسخه عمومی تنظیمات - فقط چیزی که فرانت‌اند برای تصمیم UI لازم دارد."""

    class Meta:
        model = PlatformSettings
        fields = ["multivendor_enabled"]


class VendorPublicSerializer(serializers.ModelSerializer):
    """برای نمایش عمومی فروشگاه یک فروشنده (صفحه استور، لیست محصولات و ...)."""

    class Meta:
        model = Vendor
        fields = ["id", "store_name", "store_slug", "description", "logo"]


class VendorMeSerializer(serializers.ModelSerializer):
    """فروشنده فقط می‌تواند اطلاعات نمایشی فروشگاه خودش را ویرایش کند."""

    class Meta:
        model = Vendor
        fields = [
            "id", "store_name", "store_slug", "description", "logo",
            "status", "commission_percent", "created_at",
        ]
        read_only_fields = ["id", "store_slug", "status", "commission_percent", "created_at"]


class VendorApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["store_name", "description"]


class VendorAdminSerializer(serializers.ModelSerializer):
    """برای پنل ادمین: تایید/رد فروشنده و تنظیم کارمزد اختصاصی."""

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Vendor
        fields = [
            "id", "username", "email", "store_name", "store_slug", "description",
            "logo", "status", "commission_percent", "created_at", "approved_at",
        ]
        read_only_fields = ["id", "username", "email", "store_name", "store_slug", "description", "logo", "created_at"]