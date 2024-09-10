from django.urls import path

from .views import *

app_name = 'engine'

urlpatterns = [
    path('v1/stock/', StockListAPIView.as_view()),
    path('v1/stock-price/', StockPriceListAPIView.as_view()),
    path('v1/stock-price/<int:id>/', StockPriceDetailAPIView.as_view()),
    path('v1/stock-price/now/<int:id>/', StockPriceNow.as_view()),
    path('v1/user-monitor-stock/', UserMonitorStockListAPIView.as_view()),
    path('v1/user-monitor-stock/<int:id>/', UserMonitorStockDetailAPIView.as_view()),
    path('v1/user-monitor-stock-data/', UserMonitorStockDataView.as_view()),
    path('v1/user-stock-notification-history/', UserStockNotificationHistoryListAPIView.as_view()),
    path('v1/user-stock-notification-history/<int:id>/', UserStockNotificationHistoryDetailAPIView.as_view()),
]
