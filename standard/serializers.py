from rest_framework import serializers

from .models import *


class ContactBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'user',
            'channel',
            'contact',
        ]


class StockBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'id',
            'company_name',
            'symbol',
        ]


class StockPriceBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = [
            'id',
            'stock',
            'price',
            'timestamp',
        ]


class StockPriceAggregatedSerializer(StockPriceBasicSerializer):
    stock = StockBasicSerializer()


class UserMonitorStockBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMonitorStock
        fields = [
            'id',
            'user',
            'stock',
            'interval',
            'price_limit_top',
            'price_limit_bottom',
            'notify',
            'status',
            'created_at',
            'updated_at'
        ]


class UserMonitorStockAggregatedSerializer(UserMonitorStockBasicSerializer):
    stock = StockBasicSerializer()


class UserStockNotificationHistoryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStockNotificationHistory
        fields = [
            'id',
            'user_monitor_stock',
            'interval',
            'price_limit_top',
            'price_limit_bottom',
            'created_at',
            'updated_at'
        ]


class UserStockNotificationHistoryAggregatedSerializer(UserStockNotificationHistoryBasicSerializer):
    user_monitor_stock = UserMonitorStockBasicSerializer()
