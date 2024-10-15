from rest_framework import serializers

from ..wallets.models import Wallet
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'txid', 'amount')
