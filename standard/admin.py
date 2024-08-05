from django.contrib import admin
from .models import *

admin.site.register(Contact)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(UserMonitorStock)
admin.site.register(UserStockNotificationHistory)
