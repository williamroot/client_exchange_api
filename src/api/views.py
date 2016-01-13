from .serializers import CurrencySerialiazer, ExchangeSerialiazer
from .models import Currency, Exchange
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from source.parser import Parser
from datetime import datetime, timedelta

class CurrencyList(APIView):
    def get(self, request, format=None):
        objs = Currency.objects.all()
        if not objs:
            parser = Parser()
            objs = parser.get_available_currencies()
            objs = Currency.objects.all()
        serializer = CurrencySerialiazer(objs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CurrencySerialiazer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrencyDetail(APIView):
    def get_object(self, iso_code):
        return get_object_or_404(Currency, iso_code__iexact=iso_code)

    def get(self, request, iso_code, format=None):
        obj = self.get_object(iso_code)
        obj = CurrencySerialiazer(obj)
        return Response(obj.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = CurrencySerialiazer(obj, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExchangeList(APIView):
    def get(self, request, format=None):
        objs = Exchange.objects.all()
        serializer = ExchangeSerialiazer(objs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExchangeSerialiazer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExchangeDetail(APIView):
    def get_object(self, source, target):
        """
        Exchange are valid per 1 hour.
        On each request try to get existing exchange or get new from source.
        """
        deadline = datetime.now() - timedelta(hours=1)
        source = get_object_or_404(Currency, iso_code__iexact=source)
        target = get_object_or_404(Currency, iso_code__iexact=target)
        try:
            exchage = Exchange.objects.get(
                source=source,
                target=target,
                created__gte=deadline
            )
        except Exchange.DoesNotExist:
            parser = Parser()
            exchage = parser.get_exchange(source=source,target=target)
        return exchage

    def get(self, request, source, target, format=None):
        obj = self.get_object(source, target)
        obj = ExchangeSerialiazer(obj)
        return Response(obj.data)

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = ExchangeSerialiazer(obj, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
