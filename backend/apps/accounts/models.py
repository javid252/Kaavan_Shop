from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    کاربر سفارشی سامانه. ایمیل به عنوان فیلد یکتا استفاده می‌شود
    تا هم برای ورود و هم بازیابی رمز عبور قابل استفاده باشد.
    """

    email = models.EmailField("ایمیل", unique=True)
    phone_number = models.CharField("شماره موبایل", max_length=15, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username
