import os
from selenium import webdriver
from pyvirtualdisplay import Display
from api.models import Currency, Exchange
from decimal import Decimal
import httplib
import json
import requests
from django.conf import settings


class Parser(object):
    BASE_URL = 'http://exchangeapi.williamsouza.net/api/'
    CURRENCY_URL = '{}currency'.format(BASE_URL)
    EXCHANGE_URL = BASE_URL + 'exchange/{}/{}'

    def get_auth(self):
        return requests.auth.HTTPBasicAuth(
            settings.API_USERNAME,
            settings.API_PASSWORD,
        )

    def get_available_currencies(self):
        """
        Comes the list of available currencies.
        """
        auth = self.get_auth()
        currencies = []
        content = self._get_response(
            self.CURRENCY_URL,
            auth=auth
        )
        for option in content:
            currency = Currency.objects.get_or_create(
                    iso_code=option['iso_code'],
                    name=option['name']
            )[0]
            currencies.append(currency)
        return currencies

    def get_exchange(self, source, target):
        """
        Returns the price of a currency (source) over another (target).
        """
        auth = self.get_auth()
        url = self.BASE_URL.format(source.iso_code, target.iso_code)
        content = self._get_response(self, url, auth)
        return Exchange.objects.create(
            source=source,
            target=target,
            value=Decimal(content['value']),
        )

    def _get_response(self, url, auth):
        response = requests.get(
            url,
            auth=auth
        )
        return json.loads(response.content)
