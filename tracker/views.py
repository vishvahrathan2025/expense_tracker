from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm

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

            messages.success(request, "Expense added successfully! 🎉")
            return redirect("add_expense")
    else:
        form = ExpenseForm()

    return render(request, "add_expense.html", {"form": form})


def home(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(user=request.user).order_by("-date")
    else:
        expenses = []

    total = sum(exp.amount for exp in expenses)

    # ---------------- Pie Chart ----------------
    categories = {}
    for exp in expenses:
        categories[exp.category] = categories.get(exp.category, 0) + float(exp.amount)

    pie_chart = None

    if categories:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        pie_chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close(fig)

    # ---------------- Bar Chart ----------------
    monthly_totals = {}

    for exp in expenses:
        month = exp.date.strftime("%b %Y")
        monthly_totals[month] = monthly_totals.get(month, 0) + float(exp.amount)

    bar_chart = None

    if monthly_totals:
        months = list(monthly_totals.keys())
        totals = list(monthly_totals.values())

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(months, totals)

        ax.set_title("Monthly Expenses")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")

        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        bar_chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

        buffer.close()
        plt.close(fig)

    return render(
        request,
        "home.html",
        {
            "expenses": expenses,
            "total": total,
            "pie_chart": pie_chart,
            "bar_chart": bar_chart,
        },
    )


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully! ✅")
            return redirect("home")

    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "edit_expense.html",
        {
            "form": form,
            "expense": expense,
        },
    )


@login_required
def delete_expense(request, id):
    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    expense.delete()
    messages.success(request, "Expense deleted successfully! 🗑️")

    return redirect("home")