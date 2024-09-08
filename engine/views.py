import json

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from engine.stocks.interface import StockInterface
from standard.generics import MultiSerializerListApiView, MultiSerializerDetailApiView
from standard.serializers import *


class StockListAPIView(MultiSerializerListApiView):
    permission_classes = [IsAuthenticated]
    queryset = Stock.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = StockBasicSerializer.Meta.fields
    search_fields = ["company_name", "symbol"]
    basic_serializer_class = StockBasicSerializer
    should_check_status = False


class StockPriceListAPIView(MultiSerializerListApiView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StockPrice.objects.all()
    basic_serializer_class = StockPriceBasicSerializer
    aggregated_serializer_class = StockPriceAggregatedSerializer
    should_check_status = False


class StockPriceDetailAPIView(MultiSerializerDetailApiView):
    permission_classes = [IsAuthenticated]
    queryset = StockPrice.objects.all()
    basic_serializer_class = StockPriceBasicSerializer
    aggregated_serializer_class = StockPriceAggregatedSerializer


class UserMonitorStockListAPIView(MultiSerializerListApiView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserMonitorStock.objects.all()
    basic_serializer_class = UserMonitorStockBasicSerializer
    aggregated_serializer_class = UserMonitorStockAggregatedSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data_dict = dict((key, value)  for key, value in request.data.items())
        data_dict['user'] = user.id
        serializer = self.get_serializer(data=data_dict)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class UserMonitorStockDetailAPIView(MultiSerializerDetailApiView):
    permission_classes = [IsAuthenticated]
    queryset = UserMonitorStock.objects.all()
    basic_serializer_class = UserMonitorStockBasicSerializer
    aggregated_serializer_class = UserMonitorStockAggregatedSerializer


class UserStockNotificationHistoryListAPIView(MultiSerializerListApiView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserStockNotificationHistory.objects.all()
    basic_serializer_class = UserStockNotificationHistoryBasicSerializer
    aggregated_serializer_class = UserStockNotificationHistoryAggregatedSerializer
    should_check_status = False


class UserStockNotificationHistoryDetailAPIView(MultiSerializerDetailApiView):
    permission_classes = [IsAuthenticated]
    queryset = UserStockNotificationHistory.objects.all()
    basic_serializer_class = UserStockNotificationHistoryBasicSerializer
    aggregated_serializer_class = UserStockNotificationHistoryAggregatedSerializer


class StockPriceNow(MultiSerializerListApiView):
    permission_classes = [IsAuthenticated]
    queryset = Stock.objects.all()
    basic_serializer_class = StockBasicSerializer
    should_check_status = False
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        stock_api = StockInterface()
        stock_data = stock_api.get_stock_price(instance, request.query_params.get('interval', 1))
        if stock_data:
            # copy serializer data to a dict
            serializer = dict(self.get_serializer(instance).data)
            serializer['price'] = dict(stock_data.get('results')[0]) if stock_data.get('results') else None
            return JsonResponse(serializer, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({'error': "Erro ao buscar valor do ativo"}, stock_data, status=status.HTTP_400_BAD_REQUEST)
