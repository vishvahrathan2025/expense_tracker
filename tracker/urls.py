from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.home, name="home"),

    # Expense
    path("add/", views.add_expense, name="add_expense"),
    path("edit/<int:expense_id>/", views.edit_expense, name="edit_expense"),
    path("delete/<int:expense_id>/", views.delete_expense, name="delete_expense"),
    path("budget/", views.budget, name="budget"),
    path("income/", views.income_list, name="income"),
    path("income/add/", views.add_income, name="add_income"),
    path("income/edit/<int:income_id>/", views.edit_income, name="edit_income"),
    path("income/delete/<int:income_id>/", views.delete_income, name="delete_income"),
]