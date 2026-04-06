from const.const import API_KEY
import requests

class Stock:
    current_price = 0
    high_today = 0
    low_today = 0
    open_price = 0  
    previous_close = 0
    _ticker = ""
    name = ""
    currency = "USD"

    
    def __init__(self, ticker):
        self._ticker = ticker
        self.update()


    def update_name(self):
        url = f"https://finnhub.io/api/v1/stock/profile2?symbol={self._ticker}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        self.name = data.get("name", self._ticker)

    def update(self):
        url = f"https://finnhub.io/api/v1/quote?symbol={self._ticker}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        self.current_price = round(data["c"], 2)
        self.high_today = round(data["h"], 2)
        self.low_today = round(data["l"], 2)
        self.open_price = round(data["o"], 2)
        self.previous_close = round(data["pc"], 2)
        self.update_name()
        if self.currency != "USD":
            self.exchange_to_currency()
        else:
            self.currency = "USD"


class StockTracker:
    _stocks = {}
    _currency = "USD"
    def __init__(self):
        self._stocks = {
            "AAPL": Stock("AAPL"),
            "GOOGL": Stock("GOOGL"),
            "AMZN": Stock("AMZN")
        }
        self._currency = "USD"
    
    def get_currency(self):
        return self._currency
    
    def get_stocks(self):
        return self._stocks

    def add_stock(self, ticker):
        if ticker not in self._stocks:
            self._stocks[ticker] = Stock(ticker)

    def update_all(self):
        for stock in self._stocks.values():
            stock.update()

    def exchange_currency(self, currency):
        url = f"https://open.er-api.com/v6/latest/{self._currency}"
        data = requests.get(url).json()
        rate = data["rates"][currency]

        for stock in self._stocks.values():
            stock.current_price *= rate
            stock.high_today *= rate
            stock.low_today *= rate
            stock.open_price *= rate
            stock.previous_close *= rate
            stock.currency = currency

        self._currency = currency
        


            

        
