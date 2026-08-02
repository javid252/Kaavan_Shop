from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("stores", views.PublicVendorViewSet, basename="public-vendor")

urlpatterns = [
    path("apply/", views.VendorApplyView.as_view(), name="vendor-apply"),
    path("me/", views.VendorMeView.as_view(), name="vendor-me"),
    *router.urls,
]