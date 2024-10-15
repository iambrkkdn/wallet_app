import ujson
from django.test import TestCase
from rest_framework import status

from apps.transactions import mommy_recipes as tmr
from apps.wallets import mommy_recipes as wmr


class TestWallet(TestCase):
    def setUp(self):
        self.transaction = tmr.trancation.make()
        self.wallet = wmr.wallet.make()
        self.wallet_url = "/api/wallets/"

    def test_get_wallets_ok(self):
        response = self.client.get(self.wallet_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data_out = ujson.loads(response.content)

        self.assertIn('results', data_out)
        self.assertGreaterEqual(len(data_out['results']), 1)

    def test_get_wallet_ok(self):
        response = self.client.get(f'{self.wallet_url}{self.wallet.id}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data_out = ujson.loads(response.content)

        self.assertEqual(self.wallet.id, data_out.get('id'))

    def test_create_wallet_ok(self):
        data_in = dict(label='new_label', balance=10.12)
        response = self.client.post(f'{self.wallet_url}', data=data_in, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertEqual(data_in['label'], data_out.get('label'))

    def test_delete_wallet_ok(self):
        response = self.client.delete(f'{self.wallet_url}{self.wallet.id}/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_udpate_wallet_ok(self):
        data_in = dict(label='update_label')
        response = self.client.patch(
            f'{self.wallet_url}{self.wallet.id}/',
            data=data_in,
            content_type='application/json',
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertEqual(data_in['label'], data_out.get('label'))


class TestWalletFilters(TestCase):
    def setUp(self):
        self.wallet_url = "/api/wallets/"

    def test_wallet_search_filter(self):
        wallet_1 = wmr.wallet.make(label='new_label_test1')
        wallet_2 = wmr.wallet.make(label='new_label_search_text_test2')
        search = 'text'
        response = self.client.get(f'{self.wallet_url}?search={search}')
        self.assertEqual(200, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertGreaterEqual(len(data_out['results']), 1)
        self.assertGreaterEqual(data_out['results'][0]['id'], wallet_2.id)

    def test_wallet_ordering_filter(self):
        wallet_1 = wmr.wallet.make(label='new_label_test1')
        wallet_2 = wmr.wallet.make(label='new_label_search_text_test2')
        tmr.trancation.make(wallet=wallet_1, amount=444)
        tmr.trancation.make(wallet=wallet_2, amount=333)
        response = self.client.get(f'{self.wallet_url}?ordering=balance')
        self.assertEqual(200, response.status_code)
        data_out = ujson.loads(response.content)
        self.assertGreaterEqual(len(data_out['results']), 1)
        self.assertGreaterEqual(data_out['results'][0]['id'], wallet_2.id)

    def test_wallet_limit_offset_filter(self):
        wallets = wmr.wallet.make(_quantity=50)
        response = self.client.get(f'{self.wallet_url}', {'limit': 10, 'offset': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['results'][0]['id'], wallets[0].id)
        self.assertEqual(response.data['results'][9]['id'], wallets[9].id)

        response = self.client.get(self.wallet_url, {'limit': 10, 'offset': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['results'][0]['id'], wallets[10].id)
        self.assertEqual(response.data['results'][9]['id'], wallets[19].id)

        response = self.client.get(self.wallet_url, {'limit': 15, 'offset': 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)
        self.assertEqual(response.data['results'][0]['id'], wallets[30].id)
        self.assertEqual(response.data['results'][14]['id'], wallets[44].id)

        response = self.client.get(self.wallet_url, {'limit': 10, 'offset': 45})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['results'][0]['id'], wallets[45].id)
        self.assertEqual(response.data['results'][4]['id'], wallets[49].id)
