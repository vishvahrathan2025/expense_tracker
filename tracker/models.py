from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "🍔 Food"),
        ("Travel", "🚗 Travel"),
        ("Shopping", "🛍 Shopping"),
        ("Bills", "💡 Bills"),
        ("Health", "💊 Health"),
        ("Entertainment", "🎬 Entertainment"),
        ("Education", "📚 Education"),
        ("Salary", "💼 Salary"),
        ("Investment", "📈 Investment"),
        ("Other", "📦 Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    title = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    date = models.DateField()

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class Budget(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    monthly_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.user.username} Budget"


class Income(models.Model):
    SOURCE_CHOICES = [
        ("Salary", "Salary"),
        ("Freelance", "Freelance"),
        ("Business", "Business"),
        ("Gift", "Gift"),
        ("Investment", "Investment"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField()

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.source} - ₹{self.amount}"