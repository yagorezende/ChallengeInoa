import requests
from django.conf import settings

from standard.models import Stock


class StockInterface:
    """
    Interface to interact with the stock API
    """

    api_url = "https://brapi.dev/api/"
    ticker_url = api_url + "quote/{stock_symbol}/?token={api_key}&interval={interval}"

    def __init__(self):
        self.api_key = settings.BRAPI_KEY

    def get_stock_price(self, stock: Stock, interval: int) -> dict | None:
        """
        Get stock price from the API
        :param stock: an instance of Stock
        :param interval: minutes interval for the stock price aggregation
        :return: json response from the API
        """
        url = self.ticker_url.format(stock_symbol=stock.symbol, api_key=self.api_key, interval=f"{interval}m")
        response = requests.get(url)

        if response.status_code != 200:
            return None
        return response.json()
