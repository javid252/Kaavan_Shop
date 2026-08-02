from django.contrib import admin

from .models import PlatformSettings, Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["store_name", "user", "status", "commission_percent", "created_at"]
    list_filter = ["status"]
    search_fields = ["store_name", "user__username", "user__email"]


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = ["multivendor_enabled", "default_commission_percent"]