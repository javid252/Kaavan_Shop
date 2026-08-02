from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlatformSettings, Vendor
from .permissions import IsApprovedVendor
from .serializers import (
    PlatformSettingsSerializer,
    PublicSettingsSerializer,
    VendorAdminSerializer,
    VendorApplySerializer,
    VendorMeSerializer,
    VendorPublicSerializer,
)


class PublicSettingsView(APIView):
    """فرانت‌اند با این endpoint می‌فهمد آیا حالت چندفروشندگی روشن است یا نه."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        settings_obj = PlatformSettings.load()
        return Response(PublicSettingsSerializer(settings_obj).data)


class AdminSettingsView(APIView):
    """کلید روشن/خاموش چندفروشندگی - فقط ادمین."""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(PlatformSettingsSerializer(PlatformSettings.load()).data)

    def patch(self, request):
        settings_obj = PlatformSettings.load()
        serializer = PlatformSettingsSerializer(settings_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class VendorApplyView(APIView):
    """کاربر لاگین‌کرده درخواست می‌دهد فروشنده شود؛ وضعیت 'در انتظار تایید' می‌شود."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not PlatformSettings.load().multivendor_enabled:
            return Response({"detail": "حالت چندفروشندگی در حال حاضر غیرفعال است."}, status=403)
        if hasattr(request.user, "vendor_profile"):
            return Response({"detail": "شما قبلاً برای این حساب درخواست فروشندگی ثبت کرده‌اید."}, status=400)

        serializer = VendorApplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save(user=request.user, status=Vendor.Status.PENDING)
        return Response(VendorMeSerializer(vendor).data, status=status.HTTP_201_CREATED)


class VendorMeView(APIView):
    """فروشنده اطلاعات فروشگاه خودش را می‌بیند/ویرایش می‌کند."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        vendor = getattr(request.user, "vendor_profile", None)
        if not vendor:
            return Response({"detail": "شما هنوز پروفایل فروشندگی ندارید."}, status=404)
        return Response(VendorMeSerializer(vendor).data)

    def patch(self, request):
        vendor = getattr(request.user, "vendor_profile", None)
        if not vendor:
            return Response({"detail": "شما هنوز پروفایل فروشندگی ندارید."}, status=404)
        serializer = VendorMeSerializer(vendor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PublicVendorViewSet(viewsets.ReadOnlyModelViewSet):
    """صفحه عمومی فروشگاه‌ها - فقط فروشندگان تاییدشده دیده می‌شوند."""

    queryset = Vendor.objects.filter(status=Vendor.Status.APPROVED)
    serializer_class = VendorPublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "store_slug"


class AdminVendorViewSet(viewsets.ModelViewSet):
    """پنل ادمین: لیست همه فروشندگان، تایید/رد، تنظیم کارمزد."""

    queryset = Vendor.objects.all().select_related("user")
    serializer_class = VendorAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]