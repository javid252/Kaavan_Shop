from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers

from apps.orders.models import Order
from apps.products.models import Product

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """برخلاف UserSerializer معمولی، این نسخه به ادمین اجازه تغییر is_staff/is_active را می‌دهد."""

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone_number", "is_staff", "is_active", "date_joined",
        ]
        read_only_fields = ["id", "username", "email", "date_joined"]


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        paid_orders = Order.objects.exclude(status=Order.Status.CANCELLED)
        revenue = paid_orders.aggregate(total=Sum("total_price"))["total"] or 0

        return Response({
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status=Order.Status.PENDING).count(),
            "total_users": User.objects.count(),
            "total_revenue": revenue,
            "orders_today": Order.objects.filter(created_at__date=today).count(),
            "low_stock_products": list(
                Product.objects.filter(stock__lte=5, is_active=True)
                .values("id", "name", "stock")[:5]
            ),
        })


class AdminUserViewSet(viewsets.ModelViewSet):
    """مدیریت کاربران از پنل ادمین (فعال/غیرفعال کردن، ارتقا به staff)."""

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "patch", "head", "options"]
