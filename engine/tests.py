from datetime import datetime
from pwd import struct_passwd

from django.contrib.auth import get_user_model
from django.test import TestCase, tag

from standard.models import *

TOKEN_URL = 'http://localhost:8000/api/auth/'
PRICES_URL = 'http://localhost:8000/api/v1/user-monitor-stock-data/'


# Create your tests here.
class TestModels(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='test', first_name='test',
                                                         last_name='test',
                                                         email='test@test.com')

        self.stock = Stock.objects.create(company_name='Inoa Sistemas', symbol='INOA')
        self.user_monitor_stock = UserMonitorStock.objects.create(user=self.user,
                                                                  stock=self.stock,
                                                                  status='active',
                                                                  interval=1,
                                                                  price_limit_top=10,
                                                                  price_limit_bottom=5, )
        self.stock_price = StockPrice.objects.create(stock=self.stock,
                                                     price=7,
                                                     open_price=6.5,
                                                     close_price=7.2,
                                                     high_price=8,
                                                     low_price=6.54,
                                                     timestamp=datetime.now())

    def test_get_user(self):
        self.assertTrue(get_user_model().objects.filter(username='test').exists())

    def test_create_stock(self):
        self.assertTrue(Stock.objects.filter(company_name='Inoa Sistemas', symbol='INOA').exists())

    def test_create_user_monitor_stock(self):
        self.assertTrue(UserMonitorStock.objects.filter(user=self.user,
                                                        stock=self.stock,
                                                        status='active',
                                                        interval=1,
                                                        price_limit_top=10,
                                                        price_limit_bottom=5).exists())

    def test_create_stock_price(self):
        self.assertTrue(StockPrice.objects.filter(stock=self.stock,
                                                  price=7,
                                                  open_price=6.5,
                                                  close_price=7.2,
                                                  high_price=8,
                                                  low_price=6.54).exists())

    def _get_user_auth_header(self):
        response = self.client.post(TOKEN_URL, {'username': 'test', 'password': 'test'})
        return {'Authorization': f'Token {response.json().get("token")}'}

    def test_get_user_monitor_stock_data(self):
        response = self.client.get(PRICES_URL, {'monitor': 1}, headers=self._get_user_auth_header())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('monitor_id'), 1)
        self.assertEqual(float(response.json().get('price_limit_top')), 10)
        self.assertEqual(float(response.json().get('price_limit_bottom')), 5)
        self.assertEqual(len(response.json().get('prices')), 1)
        self.assertEqual(float(response.json().get('prices')[0].get('price')), 7)
        self.assertEqual(float(response.json().get('prices')[0].get('open_price')), 6.5)
        self.assertEqual(float(response.json().get('prices')[0].get('close_price')), 7.2)
        self.assertEqual(float(response.json().get('prices')[0].get('high_price')), 8)
        self.assertEqual(float(response.json().get('prices')[0].get('low_price')), 6.54)
        self.assertIsNotNone(response.json().get('prices')[0].get('timestamp'))
