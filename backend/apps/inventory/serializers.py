from rest_framework import serializers

from apps.products.models import Product, ProductVariant

from .models import StockMovement, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "address", "is_default", "is_active", "created_at"]


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    variant_label = serializers.SerializerMethodField()
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True, default=None)
    movement_type_display = serializers.CharField(source="get_movement_type_display", read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True, default=None)

    class Meta:
        model = StockMovement
        fields = [
            "id", "product", "product_name", "variant", "variant_label", "warehouse", "warehouse_name",
            "movement_type", "movement_type_display", "quantity", "reference", "note",
            "created_by_username", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_variant_label(self, obj):
        if obj.variant:
            return f"{obj.variant.attribute_name}: {obj.variant.value}"
        return None


class StockAdjustmentSerializer(serializers.Serializer):
    """ورودی برای ثبت اصلاح دستی موجودی (نه فروش - فروش خودکار از چک‌اوت ثبت می‌شود)."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), required=False, allow_null=True)
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=False, allow_null=True)
    movement_type = serializers.ChoiceField(
        choices=[StockMovement.MovementType.RESTOCK, StockMovement.MovementType.ADJUSTMENT_IN,
                 StockMovement.MovementType.ADJUSTMENT_OUT, StockMovement.MovementType.RETURN],
    )
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(required=False, allow_blank=True)