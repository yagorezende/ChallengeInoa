from datetime import datetime

import requests
from django.conf import settings

from standard.models import Stock, StockPrice


class StockInterface:
    """
    Interface to interact with the stock API
    """

    api_url = "https://brapi.dev/api/"
    ticker_url = api_url + "quote/{stock_symbol}/"

    def __init__(self):
        self.api_key = settings.BRAPI_KEY

    def get_stock_price(self, stock: Stock, interval: int) -> dict | None:
        """
        Get stock price from the API
        :param stock: an instance of Stock
        :param interval: minutes interval for the stock price aggregation
        :return: json response from the API
        """

        params = {
            'token': self.api_key,
            'interval': f"{interval}m"
        }

        url = self.ticker_url.format(stock_symbol=stock.symbol)
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return None
        return response.json()

    def data_to_stock_price(self, stock: Stock, data: dict) -> StockPrice:
        """
        Convert the API response to a StockPrice object
        :param stock: Stock instance
        :param data: json response from the API
        :return: new StockPrice instance
        """
        return StockPrice.objects.create(
            stock=stock,
            price=data.get('regularMarketPrice'),
            open_price=data.get('regularMarketOpen'),
            close_price=data.get('regularMarketPreviousClose'),
            high_price=data.get('regularMarketDayHigh'),
            low_price=data.get('regularMarketDayLow'),
            timestamp=datetime.now()
        )
