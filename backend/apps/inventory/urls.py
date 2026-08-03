from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("warehouses", views.WarehouseViewSet, basename="warehouse")
router.register("movements", views.StockMovementViewSet, basename="stock-movement")

urlpatterns = [
    path("adjust/", views.StockAdjustmentView.as_view(), name="stock-adjust"),
    *router.urls,
]