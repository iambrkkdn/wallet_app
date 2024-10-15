from decimal import Decimal

from model_bakery.recipe import Recipe, foreign_key, seq

from apps.transactions import models as m
from apps.wallets.mommy_recipes import wallet

trancation = Recipe(
    m.Transaction,
    wallet=foreign_key(wallet),
    txid=seq('txid'),
    amount=Decimal('5000.10'),
)
