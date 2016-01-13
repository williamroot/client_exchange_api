from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
     url(r'^currency/$', views.CurrencyList.as_view(), name='currency_list'),
     url(
        r'^currency/(?P<iso_code>.+)/$',
        views.CurrencyDetail.as_view(),
        name='currency_detail'
    ),
     url(
        r'^exchange/$',
        views.ExchangeList.as_view(),
        name='exchange_list'
    ),
     url(
        r'^exchange/(?P<source>[a-z]+)/(?P<target>[a-z]+)/$',
        views.ExchangeDetail.as_view(),
        name='exchange_detail'
    )
]
