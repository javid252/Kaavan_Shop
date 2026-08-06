from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "icon", "image", "is_active", "order"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "is_main", "order"]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "product", "attribute_name", "value", "price_modifier", "stock"]


class ProductListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست/گرید محصولات."""

    category_name = serializers.CharField(source="category.name", read_only=True, default="")
    vendor_name = serializers.CharField(source="vendor.store_name", read_only=True, default=None)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "price", "discount_price", "final_price",
            "discount_percent", "in_stock", "is_featured", "category_name",
            "vendor_name", "main_image",
        ]

    def get_main_image(self, obj):
        request = self.context.get("request")
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        if main and request:
            return request.build_absolute_uri(main.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    vendor_name = serializers.CharField(source="vendor.store_name", read_only=True, default=None)
    vendor_slug = serializers.CharField(source="vendor.store_slug", read_only=True, default=None)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price", "discount_price",
            "final_price", "discount_percent", "stock", "in_stock", "is_featured",
            "category", "vendor_name", "vendor_slug", "images", "variants", "created_at",
        ]


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    برای ایجاد/ویرایش محصول.
    فیلد vendor عمداً قابل نوشتن است: در حالت چندفروشندگی، ویو مربوطه
    (ProductViewSet) این مقدار را خودش بر اساس فروشنده لاگین‌کرده تنظیم
    می‌کند تا یک فروشنده نتواند محصول را به نام فروشنده دیگری ثبت کند؛
    فقط ادمین اجازه دارد این فیلد را آزادانه از درخواست تغییر دهد.
    """

    class Meta:
        model = Product
        fields = [
            "id", "name", "category", "vendor", "description", "price",
            "discount_price", "stock", "is_active", "is_featured",
        ]