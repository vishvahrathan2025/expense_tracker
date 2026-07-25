from django import forms
from .models import Expense, Income, Budget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "title",
            "amount",
            "category",
            "date",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Expense Title"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Amount"
            }),

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Description (optional)"
            }),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            "source",
            "amount",
            "date",
            "description",
        ]

        widgets = {
            "source": forms.Select(attrs={
                "class": "form-select"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Amount"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Description (optional)"
            }),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            "monthly_budget",
        ]

        widgets = {
            "monthly_budget": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Monthly Budget"
            }),
        }

    def clean_monthly_budget(self):
        budget = self.cleaned_data["monthly_budget"]

        if budget < 0:
            raise forms.ValidationError(
                "Budget cannot be negative."
            )

        return budget