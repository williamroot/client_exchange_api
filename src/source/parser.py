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

    def get_auth(self):
        return requests.auth.HTTPBasicAuth(
            settings.API_USERNAME,
            settings.API_PASSWORD,
        )

    def get_available_currencies(self):
        """
        Comes the list of available currencies.
        """
        currencies = []
        AUTH = requests.auth.HTTPBasicAuth("william", "teste123456")
        response = requests.get(self.BASE_URL + 'currency', auth=AUTH)
        content = json.loads(response.content)
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
        url = '{}exchange/{}/{}'.format(
            self.BASE_URL, source.iso_code, target.iso_code
        )
        response = requests.get(
            url,
            auth=auth
        )
        content = json.loads(response.content)
        return Exchange.objects.create(
            source=source,
            target=target,
            value=Decimal(content['value']),
        )
