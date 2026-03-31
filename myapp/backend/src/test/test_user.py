import unittest
from unittest.mock import patch, MagicMock

from tracker.user import User


class TestUser(unittest.TestCase):

    # patch TradeHistory BEFORE User is created
    @patch("tracker.user.TradeHistory")
    def setUp(self, mock_trade_history):

        mock_trade_history.return_value = MagicMock()

        self.user = User(
            userID=1,
            l_name="Doe",
            f_name="John",
            free_fund=1000,
            invested_fund=0
        )


    # ---------- to_dict ----------
    def test_to_dict(self):

        result = self.user.to_dict()

        self.assertEqual(result["userID"], 1)
        self.assertEqual(result["l_name"], "Doe")
        self.assertEqual(result["f_name"], "John")
        self.assertEqual(result["available_fund"], 1000)
        self.assertEqual(result["invested_fund"], 0)


    # ---------- from_dict ----------
    @patch("tracker.user.TradeHistory")
    def test_from_dict(self, mock_trade_history):

        mock_trade_history.return_value = MagicMock()

        data = {
            "userID": 2,
            "last_name": "Smith",
            "first_name": "Anna",
            "available_funds": 500,
            "invested_funds": 100
        }

        user = User.from_dict(data)

        self.assertEqual(user._id, 2)
        self.assertEqual(user._l_name, "Smith")
        self.assertEqual(user._f_name, "Anna")
        self.assertEqual(user._free_fund, 500)
        self.assertEqual(user._invested_fund, 100)


    # ---------- buy success ----------
    @patch("tracker.user.get_db")
    @patch("tracker.user.TradeHistory")
    def test_buy_success(self, mock_trade_history, mock_get_db):

        mock_trade_history.return_value = MagicMock()

        mock_db = MagicMock()
        mock_cursor = MagicMock()

        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        result = self.user.buy(5, 10, "AAPL")

        self.assertTrue(result)
        self.assertEqual(self.user._free_fund, 950)
        self.assertEqual(self.user._invested_fund, 50)

        mock_db.commit.assert_called_once()


    # ---------- buy fail ----------
    def test_buy_fail_not_enough_money(self):

        result = self.user.buy(500, 10, "AAPL")

        self.assertFalse(result)


    # ---------- sell success ----------
    @patch("tracker.user.get_db")
    def test_sell_success(self, mock_get_db):

        mock_db = MagicMock()
        mock_cursor = MagicMock()

        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "total_shares": 10
        }

        result = self.user.sell(5, 10, "AAPL")

        self.assertTrue(result)


    # ---------- sell fail ----------
    @patch("tracker.user.get_db")
    def test_sell_fail_not_enough_shares(self, mock_get_db):

        mock_db = MagicMock()
        mock_cursor = MagicMock()

        mock_get_db.return_value = mock_db
        mock_db.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "total_shares": 1
        }

        result = self.user.sell(5, 10, "AAPL")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()