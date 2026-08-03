from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from apps.access.permissions import IsAdminWithModelPerm

from .models import Order
from .serializers import CheckoutSerializer, OrderSerializer, OrderStatusUpdateSerializer


class CheckoutView(generics.CreateAPIView):
    """ثبت سفارش نهایی از سبد خرید کاربر لاگین‌کرده."""

    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    """سفارش‌های کاربر جاری (برای صفحه «سفارش‌های من»)."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


class AdminOrderViewSet(viewsets.ModelViewSet):
    """مدیریت همه سفارش‌ها - فقط ادمین (پنل ادمین)."""

    queryset = Order.objects.all().prefetch_related("items").select_related("user")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminWithModelPerm]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "partial_update":
            return OrderStatusUpdateSerializer
        return OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        instance = self.get_object()

        if instance.status == Order.Status.PAID:
            self._ensure_income_transaction(instance, request.user)

        return Response(OrderSerializer(instance).data)

    @staticmethod
    def _ensure_income_transaction(order, user):
        """اگر برای این سفارش قبلاً تراکنش درآمدی ثبت نشده، یکی خودکار می‌سازد."""
        from django.utils import timezone

        from apps.accounting.models import Transaction

        if Transaction.objects.filter(related_order=order).exists():
            return
        Transaction.objects.create(
            type=Transaction.Type.INCOME,
            amount=order.total_price,
            description=f"درآمد سفارش #{order.id}",
            related_order=order,
            is_automatic=True,
            created_by=user,
            occurred_at=timezone.now().date(),
        )