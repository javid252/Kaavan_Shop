from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.permissions import IsSuperUser
from apps.orders.models import Order
from apps.products.models import Product

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """
    مدیریت کامل کاربران از پنل ادمین: فعال/غیرفعال، ارتقا به staff، و تخصیص نقش (Group).

    عمداً is_superuser را قابل‌تغییر از این API نکردیم؛ اعطای دسترسی superuser
    (که هیچ محدودیتی نمی‌شناسد) باید فقط از طریق دسترسی مستقیم به سرور/جنگو-ادمین
    انجام شود تا از افزایش سطح دسترسی (privilege escalation) از طریق API جلوگیری شود.
    """

    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)
    group_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone_number", "is_staff", "is_active", "is_superuser",
            "groups", "group_names", "date_joined",
        ]
        read_only_fields = ["id", "username", "email", "is_superuser", "date_joined"]

    def get_group_names(self, obj):
        return [g.name for g in obj.groups.all()]


class DashboardStatsView(APIView):
    """
    آمار کلی داشبورد. عمداً برای هر عضو staff باز است (فقط شمارش‌های کلی و
    بی‌خطر است)؛ محدودیت دقیق‌تر روی خودِ ماژول‌ها (محصولات، سفارش‌ها، ...) اعمال می‌شود.
    """

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
    """
    مدیریت کاربران + تخصیص نقش. چون این صفحه می‌تواند سطح دسترسی افراد را
    تغییر دهد، عمداً فقط به ادمین اصلی (superuser) محدود شده - نه هر staff ای.
    """

    queryset = User.objects.all().order_by("-date_joined").prefetch_related("groups")
    serializer_class = AdminUserSerializer
    permission_classes = [IsSuperUser]
    http_method_names = ["get", "patch", "head", "options"]