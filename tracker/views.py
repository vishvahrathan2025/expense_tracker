from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

def home(request):
    expenses = Expense.objects.filter(user=request.user) if request.user.is_authenticated else []
    total = sum(exp.amount for exp in expenses)
    return render(request, 'home.html', {'expenses': expenses, 'total': total})
