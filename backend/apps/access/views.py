from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .permissions import IsSuperUser
from .serializers import MANAGEABLE_APPS, GroupSerializer, PermissionSerializer


class PermissionCatalogueView(APIView):
    """
    فهرست همه پرمیشن‌های قابل‌واگذاری، دسته‌بندی‌شده بر اساس اپ - برای ساخت
    چک‌باکس‌های صفحه «ساخت/ویرایش نقش» در پنل ادمین استفاده می‌شود.
    """

    permission_classes = [IsSuperUser]

    def get(self, request):
        qs = (
            Permission.objects.filter(content_type__app_label__in=MANAGEABLE_APPS)
            .select_related("content_type")
            .order_by("content_type__app_label", "content_type__model", "codename")
        )
        grouped = {}
        for perm in qs:
            app = perm.content_type.app_label
            grouped.setdefault(app, []).append(PermissionSerializer(perm).data)
        return Response(grouped)


class RoleViewSet(viewsets.ModelViewSet):
    """CRUD نقش‌ها (Group های جنگو) - فقط ادمین اصلی (superuser)."""

    queryset = Group.objects.all().prefetch_related("permissions__content_type")
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser]