from django_filters import rest_framework as django_filters
from rest_framework import permissions, viewsets

from .models import Category, Product, ProductImage, ProductVariant
from .permissions import IsAdminOrReadOnly, IsAdminOrVendorOwner
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    ProductListSerializer,
    ProductVariantSerializer,
    ProductWriteSerializer,
)


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug")
    vendor = django_filters.CharFilter(field_name="vendor__store_slug")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category", "vendor", "is_featured", "is_active"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrVendorOwner]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]
    lookup_field = "slug"

    def get_queryset(self):
        qs = Product.objects.select_related("category", "vendor").prefetch_related("images", "variants")
        user = self.request.user
        is_staff = bool(user and user.is_authenticated and user.is_staff)
        vendor = getattr(user, "vendor_profile", None) if user and user.is_authenticated else None

        if is_staff:
            return qs  # ادمین همه محصولات (فعال/غیرفعال، همه فروشنده‌ها) را می‌بیند
        if vendor and self.request.query_params.get("mine") == "1":
            # فروشنده صفحه «محصولات من» را می‌خواهد: شامل غیرفعال‌های خودش هم می‌شود
            return qs.filter(vendor=vendor)
        return qs.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductWriteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        # فروشنده غیرادمین: صرف‌نظر از چیزی که در body فرستاده، فروشنده = خودش
        vendor = getattr(user, "vendor_profile", None)
        serializer.save(vendor=vendor)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
            return
        # فروشنده نمی‌تواند مالکیت محصول را به فروشنده دیگری تغییر دهد
        vendor = getattr(user, "vendor_profile", None)
        serializer.save(vendor=vendor)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser]