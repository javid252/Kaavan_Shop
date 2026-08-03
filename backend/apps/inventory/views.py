from django_filters import rest_framework as django_filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.permissions import IsAdminWithModelPerm

from .models import StockMovement, Warehouse
from .serializers import StockAdjustmentSerializer, StockMovementSerializer, WarehouseSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminWithModelPerm]


class StockMovementFilter(django_filters.FilterSet):
    product = django_filters.NumberFilter(field_name="product_id")
    warehouse = django_filters.NumberFilter(field_name="warehouse_id")
    movement_type = django_filters.CharFilter(field_name="movement_type")

    class Meta:
        model = StockMovement
        fields = ["product", "warehouse", "movement_type"]


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """دفترکل تراکنش‌های انبار - فقط خواندنی؛ ثبت از طریق StockAdjustmentView یا خودکار از چک‌اوت."""

    queryset = StockMovement.objects.select_related("product", "variant", "warehouse", "created_by")
    serializer_class = StockMovementSerializer
    permission_classes = [IsAdminWithModelPerm]
    filterset_class = StockMovementFilter


class StockAdjustmentView(APIView):
    """ثبت اصلاح دستی موجودی (ورود کالا، اصلاح افزایشی/کاهشی، مرجوعی)."""

    permission_classes = [IsAdminWithModelPerm]
    queryset = StockMovement.objects.all()  # برای اینکه IsAdminWithModelPerm بتواند مدل را تشخیص دهد

    def post(self, request):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        movement = StockMovement.record(
            product=data["product"],
            variant=data.get("variant"),
            warehouse=data.get("warehouse") or Warehouse.get_default(),
            movement_type=data["movement_type"],
            quantity=data["quantity"],
            note=data.get("note", ""),
            reference="اصلاح دستی از پنل ادمین",
            user=request.user,
        )
        return Response(StockMovementSerializer(movement).data, status=201)