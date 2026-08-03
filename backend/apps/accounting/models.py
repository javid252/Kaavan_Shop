from django.conf import settings
from django.db import models


class TransactionCategory(models.Model):
    class Type(models.TextChoices):
        INCOME = "income", "درآمد"
        EXPENSE = "expense", "هزینه"

    name = models.CharField("عنوان دسته", max_length=100)
    type = models.CharField("نوع", max_length=10, choices=Type.choices)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "دسته تراکنش مالی"
        verbose_name_plural = "دسته‌های تراکنش مالی"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """
    یک رکورد مالی (درآمد یا هزینه). تراکنش‌های درآمدی مربوط به سفارش‌ها
    خودکار وقتی وضعیت سفارش به «پرداخت شده» تغییر می‌کند ساخته می‌شوند؛
    بقیه (هزینه‌ها، درآمدهای دستی) از پنل حسابداری ثبت می‌شوند.
    """

    class Type(models.TextChoices):
        INCOME = "income", "درآمد"
        EXPENSE = "expense", "هزینه"

    type = models.CharField("نوع", max_length=10, choices=Type.choices)
    category = models.ForeignKey(
        TransactionCategory, verbose_name="دسته", related_name="transactions",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    amount = models.DecimalField("مبلغ (تومان)", max_digits=14, decimal_places=0)
    description = models.CharField("توضیح", max_length=255, blank=True)
    related_order = models.OneToOneField(
        "orders.Order", verbose_name="سفارش مرتبط", related_name="transaction",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    related_vendor = models.ForeignKey(
        "vendors.Vendor", verbose_name="فروشنده مرتبط", related_name="transactions",
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    is_automatic = models.BooleanField("ثبت خودکار سیستم", default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ثبت‌شده توسط",
        related_name="transactions", on_delete=models.SET_NULL, null=True,
    )
    occurred_at = models.DateField("تاریخ تراکنش")
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "تراکنش مالی"
        verbose_name_plural = "تراکنش‌های مالی"
        ordering = ["-occurred_at", "-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} ({self.occurred_at})"