from .models import Currency, Exchange
from rest_framework import serializers


class CurrencySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('iso_code', 'name')

class ExchangeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ('source_code', 'target_code', 'value', 'created')
