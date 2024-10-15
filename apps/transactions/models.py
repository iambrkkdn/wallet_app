from django.db import models

from apps.wallets.models import Wallet


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    class Meta:
        indexes = [
            models.Index(fields=['wallet'], name='transaction_wallet_idx'),
        ]

    def __str__(self):
        return f'{self.txid} - {self.amount}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.wallet.update_balance()
