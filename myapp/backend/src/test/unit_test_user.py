import unittest
from unittest.mock import patch, MagicMock
from tracker.user import User


class TestUserTrade(unittest.TestCase):

    # BUY TESTS

    @patch("tracker.user.get_db")
    def test_buy_success(self, mock_db):
        """CB: verify funds updated and DB commit called"""

        mock_cursor = MagicMock()
        mock_db.return_value.cursor.return_value = mock_cursor

        user = User(1, "Doe", "John", 1000, 0)

        result = user.buy(2, 100, "AAPL")

        self.assertTrue(result)
        self.assertEqual(user._free_fund, 800)
        self.assertEqual(user._invested_fund, 200)

        mock_db.return_value.commit.assert_called_once()


    @patch("tracker.user.get_db")
    def test_buy_not_enough_money(self, mock_db):
        """OB: user cannot buy stock if funds insufficient"""

        user = User(1, "Doe", "John", 50, 0)

        result = user.buy(2, 100, "AAPL")

        self.assertFalse(result)


    # SELL TESTS

    @patch("tracker.user.get_db")
    def test_sell_success(self, mock_db):
        """CB: verify selling updates funds correctly"""

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"total_shares": 10}

        mock_db.return_value.cursor.return_value = mock_cursor

        user = User(1, "Doe", "John", 500, 500)

        result = user.sell(5, 100, "AAPL")

        self.assertTrue(result)
        self.assertEqual(user._free_fund, 1000)
        self.assertEqual(user._invested_fund, 0)

        mock_db.return_value.commit.assert_called_once()


    @patch("tracker.user.get_db")
    def test_sell_not_enough_shares(self, mock_db):
        """OB: cannot sell more shares than owned"""

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"total_shares": 2}

        mock_db.return_value.cursor.return_value = mock_cursor

        user = User(1, "Doe", "John", 500, 500)

        result = user.sell(5, 100, "AAPL")

        self.assertFalse(result)


    # FROM_DICT TEST

    def test_from_dict_creates_user(self):
        """TB: verify object created from dictionary"""

        data = {
            "userID": 1,
            "last_name": "Doe",
            "first_name": "John",
            "available_funds": 1000,
            "invested_funds": 200
        }

        user = User.from_dict(data)

        self.assertEqual(user._id, 1)
        self.assertEqual(user._l_name, "Doe")
        self.assertEqual(user._f_name, "John")
        self.assertEqual(user._free_fund, 1000)
        self.assertEqual(user._invested_fund, 200)


if __name__ == "__main__":
    unittest.main()