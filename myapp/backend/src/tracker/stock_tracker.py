from const.const import API_KEY
import requests
class Stock:
    current_price = 0
    high_today = 0
    low_today = 0
    open_price = 0
    previous_close = 0
    _ticker = ""
    
    def __init__(self, ticker):
        self._ticker = ticker
        self.update()

    def update(self):
        url = f"https://finnhub.io/api/v1/quote?symbol={self._ticker}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        self.current_price = data["c"]
        self.high_today = data["h"]
        self.low_today = data["l"]
        self.open_price = data["o"]
        self.previous_close = data["pc"]

class StockTracker:
    _stocks = {}
    def __init__(self):
        self.stocks = {
            "AAPL": Stock("AAPL"),
            "GOOGL": Stock("GOOGL"),
            "AMZN": Stock("AMZN")
        }
        print("StockTracker initialized with stocks: ", list(self.stocks.keys()))

    def add_stock(self, ticker):
        if ticker not in self.stocks:
            self.stocks[ticker] = Stock(ticker)

    def update_all(self):
        for stock in self.stocks.values():
            stock.update()
    

        
