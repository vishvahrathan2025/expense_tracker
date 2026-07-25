from django.contrib import admin
from .models import Expense, Income, Budget


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "amount",
        "category",
        "date",
    )

    list_filter = (
        "category",
        "date",
    )

    search_fields = (
        "title",
        "category",
        "user__username",
    )

    ordering = ("-date",)

    list_per_page = 20


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "user",
        "amount",
        "date",
    )

    list_filter = (
        "source",
        "date",
    )

    search_fields = (
        "source",
        "user__username",
    )

    ordering = ("-date",)

    list_per_page = 20


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "monthly_budget",
    )

    search_fields = (
        "user__username",
    )