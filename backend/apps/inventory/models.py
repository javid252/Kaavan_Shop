from django.conf import settings
from django.db import models, transaction

from apps.products.models import Product, ProductVariant


class Warehouse(models.Model):
    """
    انبار فیزیکی یا مجازی. در نسخه فعلی، Product.stock همچنان «موجودی کل»
    است (برای سازگاری با سبد خرید/چک‌اوت فعلی)؛ انبارها بیشتر برای دسته‌بندی
    و آینده (تقسیم موجودی بین چند انبار) استفاده می‌شوند.
    """

    name = models.CharField("نام انبار", max_length=150)
    address = models.CharField("آدرس", max_length=255, blank=True)
    is_default = models.BooleanField("انبار پیش‌فرض", default=False)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            Warehouse.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls):
        wh = cls.objects.filter(is_default=True).first()
        if wh:
            return wh
        wh, _ = cls.objects.get_or_create(name="انبار اصلی", defaults={"is_default": True})
        return wh


class StockMovement(models.Model):
    """دفترکل تغییرات موجودی - هر افزایش/کاهش موجودی یک رکورد این‌جا ثبت می‌کند."""

    class MovementType(models.TextChoices):
        SALE = "sale", "فروش"
        RETURN = "return", "مرجوعی"
        RESTOCK = "restock", "ورود کالا / خرید"
        ADJUSTMENT_IN = "adjustment_in", "اصلاح دستی (افزایش)"
        ADJUSTMENT_OUT = "adjustment_out", "اصلاح دستی (کاهش)"

    product = models.ForeignKey(Product, verbose_name="محصول", related_name="stock_movements", on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, verbose_name="تنوع", related_name="stock_movements",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    warehouse = models.ForeignKey(
        Warehouse, verbose_name="انبار", related_name="movements",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    movement_type = models.CharField("نوع تغییر", max_length=20, choices=MovementType.choices)
    quantity = models.PositiveIntegerField("تعداد")
    reference = models.CharField("مرجع", max_length=150, blank=True, help_text="مثلاً شماره سفارش")
    note = models.TextField("توضیح", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ثبت‌شده توسط",
        related_name="stock_movements", on_delete=models.SET_NULL, null=True,
    )
    created_at = models.DateTimeField("تاریخ", auto_now_add=True)

    class Meta:
        verbose_name = "تراکنش انبار"
        verbose_name_plural = "تراکنش‌های انبار"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"

    @property
    def is_increase(self):
        return self.movement_type in (self.MovementType.RETURN, self.MovementType.RESTOCK, self.MovementType.ADJUSTMENT_IN)

    @classmethod
    @transaction.atomic
    def record(cls, *, product, movement_type, quantity, variant=None, warehouse=None, reference="", note="", user=None):
        """
        یک تراکنش انبار ثبت می‌کند و موجودی محصول/تنوع را همزمان به‌روزرسانی
        می‌کند. این نقطه واحد ورودی برای هر تغییر موجودی در کل پروژه است.
        """
        movement = cls.objects.create(
            product=product, variant=variant, warehouse=warehouse,
            movement_type=movement_type, quantity=quantity,
            reference=reference, note=note, created_by=user,
        )
        sign = 1 if movement.is_increase else -1
        if variant:
            variant.stock = max(variant.stock + sign * quantity, 0)
            variant.save(update_fields=["stock"])
        product.stock = max(product.stock + sign * quantity, 0)
        product.save(update_fields=["stock"])
        return movement