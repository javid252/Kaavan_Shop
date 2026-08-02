#!/usr/bin/env bash
# اسکریپت بیلد بک‌اند برای Render
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# دیتای نمونه فقط یک‌بار ساخته می‌شود (seed_demo از get_or_create استفاده می‌کند
# و ایمن است اگر چند بار هم اجرا شود)
python manage.py seed_demo
