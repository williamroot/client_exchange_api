from django.contrib.auth.models import User
from rest_framework.reverse import reverse
import mock
from source.parser import Parser
from models import Currency, Exchange
from views import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from decimal import Decimal

class ViewTests(APITestCase):
    """
    Test all API end points and database cache.
    Currency:
        list
        datail
    Exchange:
        list
        datail
    """
    def setUp(self):
        """
        Database startup
        """
        # user
        self.user = User.objects.create_user(
            username='test', password='password'
        )
        # currencies
        self.usd = Currency.objects.create(iso_code='USD', name='USD Dolar')
        self.brl = Currency.objects.create(iso_code='BRL', name='Real')
        self.eur = Currency.objects.create(iso_code='EUR', name='Euro')
        # exchanges
        self.exchange = Exchange.objects.create(
            source=self.usd,
            target=self.brl,
            value=Decimal(4)
        )

    @mock.patch('source.parser.Parser.get_available_currencies')
    def testCurrencyListtView(self, mock_get_currencies):
        """
        Test response for a valid request and ensure not 'source' called,
        database cache only
        """
        url = reverse('api:currency_list')
        factory = APIRequestFactory()
        view = CurrencyList.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 3)
        # ensures non source call (database cache only)
        assert not mock_get_currencies.called

    def testCurrencyDetailView(self):
        """
        Test response for a valid request
        """
        url = reverse('api:currency_detail', args=[self.usd.iso_code])
        factory = APIRequestFactory()
        view = CurrencyDetail.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request, self.usd.iso_code)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data['name'], self.usd.name)
        self.assertEqual(response.data['iso_code'], self.usd.iso_code)

    def testCurrencyNotFound(self):
        """
        Test response for a invalid request
        """
        url = reverse('api:currency_detail', args=['XXX'])
        factory = APIRequestFactory()
        view = CurrencyDetail.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request, 'XXX')
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def testExchangeListtView(self):
        """
        Test response for a valid request
        """
        url = reverse('api:exchange_list')
        factory = APIRequestFactory()
        view = ExchangeList.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data[0]['source_code'], self.usd.iso_code)
        self.assertEqual(response.data[0]['target_code'], self.brl.iso_code)

    @mock.patch('source.parser.Parser.get_exchange')
    def testExchangeDetailView(self, mock_get_exchange):
        """
        Test response for a valid request and ensure not 'source' called,
        database cache only
        """
        url = reverse(
            'api:exchange_detail',
            args={'source':self.usd.iso_code, 'target':self.brl.iso_code}
        )
        factory = APIRequestFactory()
        view = ExchangeDetail.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request, self.usd.iso_code, self.brl.iso_code)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['source_code'],
            self.exchange.source_code
        )
        self.assertEqual(
            response.data['target_code'],
            self.exchange.target_code
        )
        self.assertEqual(
            Decimal(response.data['value']),
            self.exchange.value
        )
        # ensures non source call (database cache only)
        assert not mock_get_exchange.called

    @mock.patch('source.parser.Parser.get_exchange')
    def testExchangeNotFoundValidRequest(self, mock_get_exchange):
        """
        Test response for a valid request
        Ensure: if exchange not found in database, call source to get one.
        """
        mock_get_exchange.return_value = Exchange(
            source=self.eur,
            target=self.brl,
            value=Decimal(4,20)
        )
        url = reverse(
            'api:exchange_detail',
            args={'source':'EUR', 'target':'BRL'}
        )
        factory = APIRequestFactory()
        factory = APIRequestFactory()
        view = ExchangeDetail.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(
            request,
            self.eur.iso_code,
            self.brl.iso_code
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # ensures parser called
        assert mock_get_exchange.called


    @mock.patch('source.parser.Parser.get_exchange')
    def testExchangeNotFoundInvalidRequest(self, mock_get_exchange):
        """
        Test response for a valid request
        Ensure: if exchange not found in database, call source to get one.
        """
        mock_get_exchange.return_value = Exchange(
            source=self.eur,
            target=self.brl,
            value=Decimal(4,20)
        )
        url = reverse(
            'api:exchange_detail',
            args={'source':'XXX', 'target':'DDD'}
        )
        factory = APIRequestFactory()
        factory = APIRequestFactory()
        view = ExchangeDetail.as_view()
        # Make an authenticated request to the view...
        request = factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(
            request,
            'XXX',
            'DDD'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        # ensures not parser called
        assert not  mock_get_exchange.called

