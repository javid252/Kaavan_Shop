from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("my", views.MyOrdersViewSet, basename="my-orders")

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    *router.urls,
]
