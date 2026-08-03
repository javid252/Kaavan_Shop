from django.contrib import admin

from .models import Transaction, TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "is_active"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["type", "amount", "category", "occurred_at", "is_automatic", "created_by"]
    list_filter = ["type", "is_automatic"]