from rest_framework.generics import CreateAPIView

from standard.generics import MultiSerializerListApiView, MultiSerializerDetailApiView
from standard.serializers import *


class StockListAPIView(MultiSerializerListApiView):
    queryset = Stock.objects.all()
    basic_serializer_class = StockBasicSerializer
    should_check_status = False


class StockPriceListAPIView(MultiSerializerListApiView, CreateAPIView):
    queryset = StockPrice.objects.all()
    basic_serializer_class = StockPriceBasicSerializer
    aggregated_serializer_class = StockPriceAggregatedSerializer
    should_check_status = False


class StockPriceDetailAPIView(MultiSerializerDetailApiView):
    queryset = StockPrice.objects.all()
    basic_serializer_class = StockPriceBasicSerializer
    aggregated_serializer_class = StockPriceAggregatedSerializer


class UserMonitorStockListAPIView(MultiSerializerListApiView, CreateAPIView):
    queryset = UserMonitorStock.objects.all()
    basic_serializer_class = UserMonitorStockBasicSerializer
    aggregated_serializer_class = UserMonitorStockAggregatedSerializer


class UserMonitorStockDetailAPIView(MultiSerializerDetailApiView):
    queryset = UserMonitorStock.objects.all()
    basic_serializer_class = UserMonitorStockBasicSerializer
    aggregated_serializer_class = UserMonitorStockAggregatedSerializer


class UserStockNotificationHistoryListAPIView(MultiSerializerListApiView, CreateAPIView):
    queryset = UserStockNotificationHistory.objects.all()
    basic_serializer_class = UserStockNotificationHistoryBasicSerializer
    aggregated_serializer_class = UserStockNotificationHistoryAggregatedSerializer
    should_check_status = False


class UserStockNotificationHistoryDetailAPIView(MultiSerializerDetailApiView):
    queryset = UserStockNotificationHistory.objects.all()
    basic_serializer_class = UserStockNotificationHistoryBasicSerializer
    aggregated_serializer_class = UserStockNotificationHistoryAggregatedSerializer
