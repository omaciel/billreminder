from django.db import models

class Category(models.Model):
    """
    Represents the category for a payment.
    """

    categoryName = models.CharField(
        "Category", max_length=50, null=False, blank=False
    )

    categoryColor = models.CharField(
        "Color", max_length=14, null=True, blank=True
    )

    def __unicode__(self):
        return self.categoryName

class Bill(models.Model):
    """
    Represents a payment transaction.
    """

    category = models.ForeignKey(
        Category, null=True, blank=True
    )

    payee = models.CharField(
        "Payee", max_length=50, null=False, blank=False
    )

    dueDate = models.DateTimeField(
        "Due Date", null=False, blank=False
    )

    amountDue = models.DecimalField(
        "Amount", null=False, blank=False, max_digits=19, decimal_places=2
    )

    notes = models.TextField(
        "Notes", null=True, blank=True
    )

    paid = models.BooleanField(
        "Paid", default=False
    )

    def __unicode__(self):
        return self.payee
