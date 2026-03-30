import unittest
from unittest.mock import patch
from tracker.stock_tracker import Stock, StockTracker


# Mock API responses
MOCK_QUOTE = {
    "c": 150.0,   # current price
    "h": 155.0,   # high
    "l": 145.0,   # low
    "o": 148.0,   # open
    "pc": 149.0   # previous close
}

MOCK_PROFILE = {
    "name": "Apple Inc."
}

MOCK_EXCHANGE = {
    "rates": {
        "CAD": 1.35
    }
}


class TestStock(unittest.TestCase):

    @patch("requests.get")
    def test_stock_update_sets_prices(self, mock_get):
        """CB: verifies internal attributes updated correctly"""

        # configure mock responses
        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE)
        ]

        stock = Stock("AAPL")

        self.assertEqual(stock.current_price, 150.0)
        self.assertEqual(stock.high_today, 155.0)
        self.assertEqual(stock.low_today, 145.0)
        self.assertEqual(stock.open_price, 148.0)
        self.assertEqual(stock.previous_close, 149.0)


    @patch("requests.get")
    def test_stock_update_name(self, mock_get):
        """TB: verify company name updated"""

        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE)
        ]

        stock = Stock("AAPL")

        self.assertEqual(stock.name, "Apple Inc.")


class TestStockTracker(unittest.TestCase):

    @patch("requests.get")
    def test_tracker_initializes_with_default_stocks(self, mock_get):
        """OB: verify default stocks exist"""

        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE)
        ]

        tracker = StockTracker()

        stocks = tracker.get_stocks()

        self.assertIn("AAPL", stocks)
        self.assertIn("GOOGL", stocks)
        self.assertIn("AMZN", stocks)


    @patch("requests.get")
    def test_add_stock(self, mock_get):
        """OB: verify stock added successfully"""

        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE)
        ]

        tracker = StockTracker()
        tracker.add_stock("TSLA")

        self.assertIn("TSLA", tracker.get_stocks())


    @patch("requests.get")
    def test_exchange_currency(self, mock_get):
        """CB: verify currency conversion applied correctly"""

        mock_get.side_effect = [
            # initial stock creation calls
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),

            # exchange rate call
            unittest.mock.Mock(json=lambda: MOCK_EXCHANGE)
        ]

        tracker = StockTracker()
        tracker.exchange_currency("CAD")

        stock = tracker.get_stocks()["AAPL"]

        self.assertEqual(stock.currency, "CAD")
        self.assertAlmostEqual(stock.current_price, 150.0 * 1.35)


    @patch("requests.get")
    def test_update_all_updates_each_stock(self, mock_get):
        """TB: verify update_all refreshes stock values"""

        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),

            # updates again
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
            unittest.mock.Mock(json=lambda: MOCK_QUOTE),
            unittest.mock.Mock(json=lambda: MOCK_PROFILE),
        ]

        tracker = StockTracker()

        tracker.update_all()

        for stock in tracker.get_stocks().values():
            self.assertEqual(stock.current_price, 150.0)


if __name__ == "__main__":
    unittest.main()