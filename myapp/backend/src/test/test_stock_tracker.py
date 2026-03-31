import unittest
from unittest.mock import Mock, patch

from tracker.stock_tracker import Stock, StockTracker


# -------------------------
# Mock API responses
# -------------------------

MOCK_QUOTE = {
    "c": 150.0,
    "h": 155.0,
    "l": 145.0,
    "o": 148.0,
    "pc": 149.0
}

MOCK_PROFILE = {
    "name": "Apple Inc."
}

MOCK_HISTORY = {
    "Monthly Time Series": {
        "2025-01-31": {
            "1. open": "100.00",
            "4. close": "110.00"
        },
        "2024-12-31": {
            "1. open": "95.00",
            "4. close": "105.00"
        }
    }
}

MOCK_EXCHANGE = {
    "rates": {
        "CAD": 1.35
    }
}


# -------------------------
# Helper function
# Each Stock creation needs 3 API calls:
# 1 quote
# 1 profile
# 1 history
# -------------------------

def stock_api_calls():
    return [
        Mock(json=lambda: MOCK_QUOTE),
        Mock(json=lambda: MOCK_PROFILE),
        Mock(json=lambda: MOCK_HISTORY),
    ]


# -------------------------
# Stock Tests
# -------------------------

class TestStock(unittest.TestCase):

    @patch("tracker.stock_tracker.requests.get")
    def test_stock_update_sets_prices(self, mock_get):
        """CB: verify internal values update correctly"""

        mock_get.side_effect = stock_api_calls()

        stock = Stock("AAPL")

        self.assertEqual(stock.current_price, 150.0)
        self.assertEqual(stock.high_today, 155.0)
        self.assertEqual(stock.low_today, 145.0)
        self.assertEqual(stock.open_price, 148.0)
        self.assertEqual(stock.previous_close, 149.0)


    @patch("tracker.stock_tracker.requests.get")
    def test_stock_update_name(self, mock_get):
        """TB: verify company name retrieved"""

        mock_get.side_effect = stock_api_calls()

        stock = Stock("AAPL")

        self.assertEqual(stock.name, "Apple Inc.")


    @patch("tracker.stock_tracker.requests.get")
    def test_get_stock_history(self, mock_get):
        """CB: verify monthly history stored"""

        mock_get.side_effect = stock_api_calls()

        stock = Stock("AAPL")

        history = stock._history

        self.assertEqual(
            history["close"],
            ["110.00", "105.00"]
        )

        self.assertEqual(
            history["open"],
            ["100.00", "95.00"]
        )


# -------------------------
# StockTracker Tests
# -------------------------

class TestStockTracker(unittest.TestCase):

    @patch("tracker.stock_tracker.requests.get")
    def test_tracker_initializes_with_default_stocks(self, mock_get):
        """OB: default stocks exist"""

        mock_get.side_effect = stock_api_calls() * 3

        tracker = StockTracker()

        stocks = tracker.get_stocks()

        self.assertIn("AAPL", stocks)
        self.assertIn("GOOGL", stocks)
        self.assertIn("AMZN", stocks)


    @patch("tracker.stock_tracker.requests.get")
    def test_add_stock(self, mock_get):
        """OB: stock added successfully"""

        mock_get.side_effect = stock_api_calls() * 4

        tracker = StockTracker()

        tracker.add_stock("TSLA")

        self.assertIn("TSLA", tracker.get_stocks())


    @patch("tracker.stock_tracker.requests.get")
    def test_exchange_currency(self, mock_get):
        """CB: verify currency conversion"""

        mock_get.side_effect = (
            stock_api_calls() * 3
            + [Mock(json=lambda: MOCK_EXCHANGE)]
        )

        tracker = StockTracker()

        tracker.exchange_currency("CAD")

        stock = tracker.get_stocks()["AAPL"]

        self.assertEqual(stock.currency, "CAD")

        self.assertAlmostEqual(
            stock.current_price,
            150.0 * 1.35
        )


    @patch("tracker.stock_tracker.requests.get")
    def test_update_all_updates_each_stock(self, mock_get):
        """TB: update_all refreshes stocks"""

        mock_get.side_effect = stock_api_calls() * 6

        tracker = StockTracker()

        tracker.update_all()

        for stock in tracker.get_stocks().values():
            self.assertEqual(stock.current_price, 150.0)


if __name__ == "__main__":
    unittest.main()