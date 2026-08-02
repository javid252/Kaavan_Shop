from rest_framework import serializers


class CartLineInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1)


class CartValidateSerializer(serializers.Serializer):
    items = CartLineInputSerializer(many=True)
