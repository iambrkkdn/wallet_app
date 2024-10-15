from decimal import Decimal

import ujson
from django.test import TestCase
from rest_framework import status

from apps.transactions import mommy_recipes as tmr
from apps.wallets import mommy_recipes as wmr
from apps.wallets.models import Wallet


class TestTransaction(TestCase):
    def setUp(self):
        self.transaction = tmr.trancation.make()
        self.wallet = wmr.wallet.make()
        self.transaction_url = "/api/transactions/"

    def test_get_transactions_ok(self):
        response = self.client.get(self.transaction_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data_out = ujson.loads(response.content)

        self.assertIn('results', data_out)
        self.assertGreaterEqual(len(data_out['results']), 1)

    def test_get_transaction_ok(self):
        response = self.client.get(f'{self.transaction_url}{self.transaction.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data_out = ujson.loads(response.content)

        self.assertEqual(self.transaction.id, data_out.get('id'))

    def test_create_transaction_ok(self):
        data_in = dict(wallet=self.wallet.id, txid='testtxtid', amount=10.1)
        response = self.client.post(f'{self.transaction_url}', data=data_in)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertEqual(data_in['wallet'], data_out.get('wallet'))
        self.assertEqual(data_in['txid'], data_out.get('txid'))

    def test_delete_transaction_ok(self):
        response = self.client.delete(f'{self.transaction_url}{self.transaction.id}/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_udpate_transaction_ok(self):
        wallet_to_update = wmr.wallet.make()
        data_in = dict(wallet=wallet_to_update.id)
        response = self.client.patch(
            f'{self.transaction_url}{self.transaction.id}/',
            data=data_in,
            content_type='application/json',
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertEqual(wallet_to_update.id, data_out.get('wallet'))

    def test_create_transactions_wallet_balance_ok(self):
        data_in_1 = dict(wallet=self.wallet.id, txid='testtxtid1', amount=10.1)
        response_1 = self.client.post(f'{self.transaction_url}', data=data_in_1)
        self.assertEqual(status.HTTP_201_CREATED, response_1.status_code)

        data_in_2 = dict(wallet=self.wallet.id, txid='testtxtid2', amount=30.1)
        response_2 = self.client.post(f'{self.transaction_url}', data=data_in_2)
        self.assertEqual(status.HTTP_201_CREATED, response_2.status_code)

        wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(wallet.balance, Decimal(str(data_in_1['amount'] + data_in_2['amount'])))


class TestTransactionFilters(TestCase):
    def setUp(self):
        self.transaction_url = "/api/transactions/"

    def test_transactoin_filter_ok(self):
        transaction_1 = tmr.trancation.make()
        transaction_2 = tmr.trancation.make()
        response = self.client.get(f'{self.transaction_url}?wallet={transaction_2.wallet.id}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertGreaterEqual(len(data_out['results']), 1)
        self.assertGreaterEqual(data_out['results'][0]['id'], transaction_2.id)

    def test_wallet_ordering_filter(self):
        transaction_1 = tmr.trancation.make(amount=1123)
        transaction_2 = tmr.trancation.make(amount=3333)
        response = self.client.get(f'{self.transaction_url}?ordering=amount')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertGreaterEqual(len(data_out['results']), 1)
        self.assertGreaterEqual(data_out['results'][0]['id'], transaction_1.id)

    def test_wallet_limit_offset_filter(self):
        trancations = tmr.trancation.make(_quantity=50)
        response = self.client.get(f'{self.transaction_url}', {'limit': 10, 'offset': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['results'][0]['id'], trancations[0].id)
        self.assertEqual(response.data['results'][9]['id'], trancations[9].id)

        response = self.client.get(self.transaction_url, {'limit': 10, 'offset': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['results'][0]['id'], trancations[10].id)
        self.assertEqual(response.data['results'][9]['id'], trancations[19].id)

        response = self.client.get(self.transaction_url, {'limit': 15, 'offset': 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)
        self.assertEqual(response.data['results'][0]['id'], trancations[30].id)
        self.assertEqual(response.data['results'][14]['id'], trancations[44].id)

        response = self.client.get(self.transaction_url, {'limit': 10, 'offset': 45})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['results'][0]['id'], trancations[45].id)
        self.assertEqual(response.data['results'][4]['id'], trancations[49].id)
