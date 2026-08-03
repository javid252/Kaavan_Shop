from django.contrib import admin

from .models import StockMovement, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "is_default", "is_active"]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["product", "movement_type", "quantity", "warehouse", "created_by", "created_at"]
    list_filter = ["movement_type"]
    readonly_fields = [f.name for f in StockMovement._meta.fields]