from django.test import TestCase
from api.models import Currency, Exchange
from parser import Parser
from decimal import Decimal

class GetExchangeTest(TestCase):
    def setUp(self):
        self.source = Currency.objects.get_or_create(
            iso_code='USD',
        )[0]
        self.target = Currency.objects.get_or_create(
            iso_code='BRL',
        )[0]

    def test_get_exchange(self):
        parser = Parser()
        exchange = parser.get_exchange(source=self.source, target=self.target)
        self.assertTrue(isinstance(exchange, Exchange))
        self.assertTrue(exchange.value > Decimal(0))


class GetCurrenciesTest(TestCase):
    def test_get_currencies(self):
        parser = Parser()
        currencies = parser.get_available_currencies()
        self.assertTrue(isinstance(currencies[0],Currency))



