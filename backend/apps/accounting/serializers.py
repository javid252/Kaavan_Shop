from django.utils import timezone
from rest_framework import serializers

from .models import Transaction, TransactionCategory


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ["id", "name", "type", "is_active"]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True, default=None)
    vendor_name = serializers.CharField(source="related_vendor.store_name", read_only=True, default=None)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True, default=None)

    class Meta:
        model = Transaction
        fields = [
            "id", "type", "category", "category_name", "amount", "description",
            "related_order", "related_vendor", "vendor_name", "is_automatic",
            "created_by_username", "occurred_at", "created_at",
        ]
        read_only_fields = ["id", "is_automatic", "created_at"]

    def validate(self, attrs):
        if attrs.get("related_order") and not self.instance:
            if Transaction.objects.filter(related_order=attrs["related_order"]).exists():
                raise serializers.ValidationError("برای این سفارش قبلاً یک تراکنش ثبت شده است.")
        return attrs

    def create(self, validated_data):
        validated_data.setdefault("occurred_at", timezone.now().date())
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class AccountingSummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=14, decimal_places=0)
    total_expense = serializers.DecimalField(max_digits=14, decimal_places=0)
    net_profit = serializers.DecimalField(max_digits=14, decimal_places=0)
    by_category = serializers.ListField()