from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


class Wallet(models.Model):
    label = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['label'], name='wallet_label_idx'),
        ]

    def __str__(self):
        return self.label

    def update_balance(self):
        total_balance = self.transactions.aggregate(total=Sum('amount'))['total'] or 0
        if total_balance < 0:
            raise ValidationError("Wallet balance should never be negative.")
        self.balance = total_balance
        self.save()
