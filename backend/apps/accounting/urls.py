from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("categories", views.TransactionCategoryViewSet, basename="transaction-category")
router.register("transactions", views.TransactionViewSet, basename="transaction")

urlpatterns = [
    path("summary/", views.AccountingSummaryView.as_view(), name="accounting-summary"),
    *router.urls,
]