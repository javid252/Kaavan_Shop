from django.conf import settings
from django.db import models

from apps.products.models import Product, ProductVariant


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در حال بررسی"
        PAID = "paid", "پرداخت شده"
        SHIPPED = "shipped", "ارسال شده"
        DELIVERED = "delivered", "تحویل شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE,
    )
    status = models.CharField("وضعیت", max_length=20, choices=Status.choices, default=Status.PENDING)
    full_name = models.CharField("نام گیرنده", max_length=150)
    phone_number = models.CharField("شماره موبایل", max_length=15)
    address = models.TextField("آدرس تحویل")
    postal_code = models.CharField("کد پستی", max_length=10, blank=True)
    total_price = models.DecimalField("مبلغ کل (تومان)", max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش #{self.id} - {self.user}"

    def recalculate_total(self):
        self.total_price = sum(item.line_total for item in self.items.all())
        self.save(update_fields=["total_price"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(
        ProductVariant, related_name="order_items", on_delete=models.SET_NULL, null=True, blank=True,
    )
    vendor = models.ForeignKey(
        "vendors.Vendor", verbose_name="فروشنده", related_name="order_items",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    product_name = models.CharField("نام محصول (در زمان خرید)", max_length=200)
    variant_label = models.CharField("مشخصات تنوع", max_length=100, blank=True)
    unit_price = models.DecimalField("قیمت واحد", max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField("تعداد")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
