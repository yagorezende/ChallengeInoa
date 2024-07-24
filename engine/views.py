from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from standard.generics import MultiSerializerListApiView, MultiSerializerDetailApiView
from standard.serializers import *


class StockListAPIView(MultiSerializerListApiView):
    permission_classes = [IsAuthenticated]
    queryset = Stock.objects.all()
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
