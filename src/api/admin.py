from django.contrib import admin
from models import Currency, Exchange

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code',)
    model = Currency

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('source', 'target', 'value', 'created',)
    model = Exchange

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Exchange, ExchangeAdmin)
