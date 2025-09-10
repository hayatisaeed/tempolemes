from django.db import models
from crm.models import Customer


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)

    receipt_text = models.TextField(blank=True, null=True)
    receipt_file = models.FileField(upload_to='payment_receipts/', blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.timestamp}"
    

class Installment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)

    due_date = models.DateField()

    paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    related_payments = models.ManyToManyField(Payment, blank=True)

    paid_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Installment for {self.customer.name} - {self.total_amount}"
