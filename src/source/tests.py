from django.test import TestCase
from api.models import Currency, Exchange
from parser import Parser
from decimal import Decimal
import mock
import requests_mock
import requests
import json

class GetExchangeTest(TestCase):
    def setUp(self):
        self.source = Currency.objects.get_or_create(
            iso_code='USD',
        )[0]
        self.target = Currency.objects.get_or_create(
            iso_code='BRL',
        )[0]
        self.currencies = [self.source, self.target]

    @mock.patch('source.parser.Parser._get_response')
    def test_get_exchange(self, mock_response):
        parser = Parser()
        mock_response.return_value = {'value': 4}
        exchange = parser.get_exchange(
            source=self.source,
            target=self.target
        )
        self.assertTrue(isinstance(exchange, Exchange))
        self.assertTrue(exchange.value == 4)

    @mock.patch('source.parser.Parser._get_response')
    def test_get_currencies(self, mock_response):
        mock_response.return_value = map(lambda x:{
            'iso_code': x.iso_code,
            'name': x.name
        }, self.currencies)
        parser = Parser()
        currencies = parser.get_available_currencies()
        self.assertEqual(currencies, self.currencies)
        assert mock_response.clalled





