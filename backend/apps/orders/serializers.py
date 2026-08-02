from rest_framework import serializers

from apps.products.models import Product, ProductVariant

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "variant_label", "unit_price", "quantity", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    user_display = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "user_display", "status", "status_display", "full_name", "phone_number",
            "address", "postal_code", "total_price", "items", "created_at", "updated_at",
        ]
        read_only_fields = ["status", "total_price", "created_at", "updated_at"]


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]


class CheckoutLineSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    """ورودی ثبت سفارش: اطلاعات گیرنده + آیتم‌های سبد خرید کلاینت."""

    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.CharField()
    postal_code = serializers.CharField(max_length=10, required=False, allow_blank=True)
    items = CheckoutLineSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("سبد خرید خالی است.")
        return items

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(user=user, **validated_data)

        for line in items_data:
            product = Product.objects.filter(pk=line["product_id"], is_active=True).first()
            if not product:
                continue
            variant = None
            if line.get("variant_id"):
                variant = ProductVariant.objects.filter(pk=line["variant_id"], product=product).first()

            available = variant.stock if variant else product.stock
            quantity = min(line["quantity"], available)
            if quantity <= 0:
                continue

            unit_price = product.final_price + (variant.price_modifier if variant else 0)
            OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                vendor=product.vendor,
                product_name=product.name,
                variant_label=f"{variant.attribute_name}: {variant.value}" if variant else "",
                unit_price=unit_price,
                quantity=quantity,
            )

            if variant:
                variant.stock -= quantity
                variant.save(update_fields=["stock"])
            product.stock = max(product.stock - quantity, 0)
            product.save(update_fields=["stock"])

        order.recalculate_total()
        return order
