from django.db import models


class AccessControl(models.Model):
    """
    این مدل هیچ جدولی در دیتابیس نمی‌سازد (managed=False) — فقط برای تعریف
    Permission های سفارشی سطح‌بالا استفاده می‌شود که به یک مدل مشخص مربوط
    نیستند (مثلاً «مدیریت نقش‌ها» یا «تغییر تنظیمات کلی سایت»).
    این الگوی رایج در جنگو برای permission های عمومی است.
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ("manage_roles", "می‌تواند نقش‌ها و دسترسی‌های کاربران را مدیریت کند"),
            ("manage_platform_settings", "می‌تواند تنظیمات کلی پلتفرم را تغییر دهد"),
        ]