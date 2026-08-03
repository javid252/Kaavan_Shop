from django.db.models import Sum
from django_filters import rest_framework as django_filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.access.permissions import IsAdminWithModelPerm

from .models import Transaction, TransactionCategory
from .serializers import TransactionCategorySerializer, TransactionSerializer


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAdminWithModelPerm]


class TransactionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="occurred_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="occurred_at", lookup_expr="lte")
    type = django_filters.CharFilter(field_name="type")
    category = django_filters.NumberFilter(field_name="category_id")

    class Meta:
        model = Transaction
        fields = ["date_from", "date_to", "type", "category"]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("category", "related_vendor", "created_by")
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminWithModelPerm]
    filterset_class = TransactionFilter

    def get_serializer_context(self):
        return {"request": self.request}


class AccountingSummaryView(APIView):
    """خلاصه مالی: کل درآمد، کل هزینه، سود خالص، و تفکیک بر اساس دسته - در یک بازه زمانی."""

    permission_classes = [IsAdminWithModelPerm]
    queryset = Transaction.objects.all()

    def get(self, request):
        qs = Transaction.objects.all()
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from:
            qs = qs.filter(occurred_at__gte=date_from)
        if date_to:
            qs = qs.filter(occurred_at__lte=date_to)

        total_income = qs.filter(type=Transaction.Type.INCOME).aggregate(s=Sum("amount"))["s"] or 0
        total_expense = qs.filter(type=Transaction.Type.EXPENSE).aggregate(s=Sum("amount"))["s"] or 0

        by_category = list(
            qs.values("category__id", "category__name", "type")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": total_income - total_expense,
            "by_category": by_category,
        })