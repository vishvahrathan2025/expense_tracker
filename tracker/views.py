from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')  # Important: for rendering charts without a GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def add_expense(request):
    if request.method == 'POST':
        # your existing save logic
        # Example:
        Expense.objects.create(
            user=request.user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            category=request.POST['category'],
            date=request.POST['date'],
            description=request.POST.get('description', '')
        )
        messages.success(request, "Expense added successfully! 🎉")
        return redirect('add_expense')

    return render(request, 'add_expense.html')

def home(request):
    expenses = Expense.objects.filter(user=request.user) if request.user.is_authenticated else []
    total = sum(exp.amount for exp in expenses)
    categories = {}
    for exp in expenses:
        categories[exp.category] = categories.get(exp.category, 0) + float(exp.amount)

    chart = None
    if categories:
        fig, ax = plt.subplots()
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is circular

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        chart = base64.b64encode(image_png).decode('utf-8')
        plt.close(fig)
        monthly_totals = {}
    for exp in expenses:
        month_name = exp.date.strftime('%b %Y')  # e.g., "Oct 2025"
        monthly_totals[month_name] = monthly_totals.get(month_name, 0) + float(exp.amount)

    bar_chart = None
    if monthly_totals:
        months = list(monthly_totals.keys())
        totals = list(monthly_totals.values())

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(months, totals, color='skyblue')
        ax.set_title('Monthly Expenses')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (₹)')
        plt.xticks(rotation=45, ha='right')

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        bar_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

    return render(request, 'home.html', {
        'expenses': expenses,
        'total': total,
        'pie_chart': chart,
        'bar_chart': bar_chart
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expense

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.description = request.POST.get('description', '')
        expense.save()

        messages.success(request, "Expense updated successfully! ✨")
        return redirect('home')

    expenses = Expense.objects.all()
    return render(request, 'home.html', {'expenses': expenses})
