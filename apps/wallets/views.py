from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('label',)
    ordering_fields = ('balance',)
