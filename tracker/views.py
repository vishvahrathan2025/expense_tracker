from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .models import Expense, Income, Budget
from .forms import ExpenseForm, IncomeForm, BudgetForm

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from io import BytesIO
import base64

@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            messages.success(
                request,
                "Expense added successfully! 🎉"
            )

            return redirect("home")

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = ExpenseForm()

    return render(
        request,
        "add_expense.html",
        {
            "form": form,
        },
    )

@login_required
def home(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    incomes = Income.objects.filter(
        user=request.user
    )

    # ----------------------------
    # SEARCH
    # ----------------------------

    search = request.GET.get("search")

    if search:
        expenses = expenses.filter(
            title__icontains=search
        )

    # ----------------------------
    # CATEGORY FILTER
    # ----------------------------

    category = request.GET.get("category")

    if category:
        expenses = expenses.filter(
            category=category
        )

    # ----------------------------
    # TOTALS
    # ----------------------------

    total_expense = (
        expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    total_income = (
        incomes.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    balance = total_income - total_expense

    # ----------------------------
    # BUDGET
    # ----------------------------

    budget, created = Budget.objects.get_or_create(
        user=request.user
    )

    budget_used = 0

    if budget.monthly_budget > 0:

        budget_used = min(
            100,
            (float(total_expense) /
             float(budget.monthly_budget)) * 100
        )

    # ----------------------------
    # PIE CHART
    # ----------------------------

    categories = {}

    for expense in expenses:
        categories[expense.category] = (
            categories.get(expense.category, 0)
            + float(expense.amount)
        )

    pie_chart = None

    if categories:

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        buffer = BytesIO()

        plt.tight_layout()

        plt.savefig(
            buffer,
            format="png"
        )

        buffer.seek(0)

        pie_chart = base64.b64encode(
            buffer.getvalue()
        ).decode()

        buffer.close()

        plt.close(fig)

    # ----------------------------
    # MONTHLY BAR GRAPH
    # ----------------------------

    monthly = {}

    for expense in expenses:

        month = expense.date.strftime("%b %Y")

        monthly[month] = (
            monthly.get(month, 0)
            + float(expense.amount)
        )

    bar_chart = None

    if monthly:

        months = list(monthly.keys())

        totals = list(monthly.values())

        fig, ax = plt.subplots(
            figsize=(7,4)
        )

        ax.bar(
            months,
            totals
        )

        ax.set_title(
            "Monthly Expenses"
        )

        ax.set_ylabel(
            "Amount (₹)"
        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png"
        )

        buffer.seek(0)

        bar_chart = base64.b64encode(
            buffer.getvalue()
        ).decode()

        buffer.close()

        plt.close(fig)

    # ----------------------------
    # TOP CATEGORY
    # ----------------------------

    top_category = "-"

    if categories:

        top_category = max(
            categories,
            key=categories.get
        )

    return render(
        request,
        "home.html",
        {

            "expenses": expenses,

            "total_expense": total_expense,

            "total_income": total_income,

            "balance": balance,

            "budget": budget,

            "budget_used": budget_used,

            "top_category": top_category,

            "pie_chart": pie_chart,

            "bar_chart": bar_chart,

            "categories": Expense.CATEGORY_CHOICES,
        },
    )


@login_required
@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Expense updated successfully!"
            )

            return redirect("home")

        messages.error(
            request,
            "Please fix the errors."
        )

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        "edit_expense.html",
        {
            "form": form,
            "expense": expense,
        },
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        expense.delete()

        messages.success(
            request,
            "Expense deleted successfully."
        )

        return redirect("home")

    return render(
        request,
        "delete_expense.html",
        {
            "expense": expense
        }
    )
@login_required
def budget(request):

    budget, created = Budget.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = BudgetForm(
            request.POST,
            instance=budget
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Budget updated successfully!"
            )

            return redirect("budget")

    else:

        form = BudgetForm(
            instance=budget
        )

    total_expense = Expense.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    remaining = budget.monthly_budget - total_expense

    percent = 0

    if budget.monthly_budget > 0:

        percent = min(
            100,
            float(total_expense) /
            float(budget.monthly_budget) * 100
        )

    return render(
        request,
        "budget.html",
        {
            "form": form,
            "budget": budget,
            "total_expense": total_expense,
            "remaining": remaining,
            "percent": percent,
        }
    )
@login_required
def income_list(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-date")

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "income.html",
        {
            "incomes": incomes,
            "total_income": total_income,
        },
    )


@login_required
def add_income(request):

    if request.method == "POST":

        form = IncomeForm(request.POST)

        if form.is_valid():

            income = form.save(commit=False)
            income.user = request.user
            income.save()

            messages.success(
                request,
                "Income added successfully!"
            )

            return redirect("income")

    else:

        form = IncomeForm()

    return render(
        request,
        "add_income.html",
        {
            "form": form
        },
    )


@login_required
def edit_income(request, income_id):

    income = get_object_or_404(
        Income,
        id=income_id,
        user=request.user
    )

    if request.method == "POST":

        form = IncomeForm(
            request.POST,
            instance=income
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Income updated successfully!"
            )

            return redirect("income")

    else:

        form = IncomeForm(instance=income)

    return render(
        request,
        "edit_income.html",
        {
            "form": form
        },
    )


@login_required
def delete_income(request, income_id):

    income = get_object_or_404(
        Income,
        id=income_id,
        user=request.user
    )

    if request.method == "POST":

        income.delete()

        messages.success(
            request,
            "Income deleted."
        )

        return redirect("income")

    return render(
        request,
        "delete_income.html",
        {
            "income": income
        },
    )