from decimal import Decimal

from model_bakery.recipe import Recipe, seq

from apps.wallets import models as m

wallet = Recipe(
    m.Wallet,
    label=seq('label'),
    balance=Decimal('10000.10'),
)
