from rest_framework import serializers

from apps.transactions.serializers import TransactionSerializer

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'label', 'balance', 'transactions')
