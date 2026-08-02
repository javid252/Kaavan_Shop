from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, ProductVariant

from .serializers import CartValidateSerializer


class CartValidateView(APIView):
    """
    سبد خرید در فرانت‌اند (Vuex + localStorage) نگه‌داری می‌شود.
    این endpoint فقط لیست آیتم‌ها را می‌گیرد و قیمت/موجودی واقعی از دیتابیس
    را برمی‌گرداند تا کاربر همیشه قیمت و موجودی صحیح را ببیند (نه قیمتی که
    ممکن است در حافظه مرورگر قدیمی شده باشد).
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CartValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lines = []
        subtotal = 0
        has_issue = False

        for item in serializer.validated_data["items"]:
            product = Product.objects.filter(pk=item["product_id"], is_active=True).first()
            if not product:
                lines.append({
                    "product_id": item["product_id"], "valid": False,
                    "reason": "محصول یافت نشد یا غیرفعال است.",
                })
                has_issue = True
                continue

            variant = None
            if item.get("variant_id"):
                variant = ProductVariant.objects.filter(pk=item["variant_id"], product=product).first()

            available_stock = variant.stock if variant else product.stock
            unit_price = float(product.final_price) + (float(variant.price_modifier) if variant else 0)
            quantity = min(item["quantity"], available_stock) if available_stock else 0
            valid = available_stock > 0 and quantity == item["quantity"]

            line_total = unit_price * quantity
            subtotal += line_total
            if not valid:
                has_issue = True

            lines.append({
                "product_id": product.id,
                "product_name": product.name,
                "product_slug": product.slug,
                "variant_id": variant.id if variant else None,
                "variant_label": f"{variant.attribute_name}: {variant.value}" if variant else None,
                "unit_price": unit_price,
                "requested_quantity": item["quantity"],
                "available_stock": available_stock,
                "quantity": quantity,
                "line_total": line_total,
                "valid": valid,
            })

        return Response({
            "items": lines,
            "subtotal": subtotal,
            "has_issue": has_issue,
        })
