import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# ---------------------------------------------------------------------------
# Path setup — mirrors how the other test files are run from the test/ dir
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# user_api.py instantiates StockTracker() at module level, which fires a
# live network call. We patch it in sys.modules BEFORE the import so the
# module never reaches the real constructor.
# ---------------------------------------------------------------------------
mock_stock_tracker = MagicMock()
mock_stock_tracker_class = MagicMock(return_value=mock_stock_tracker)
sys.modules.setdefault("tracker.stock_tracker", MagicMock(StockTracker=mock_stock_tracker_class))

# Now it's safe to import the blueprint
from flask import Flask
from routes.user_api import user_bp


def make_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.secret_key = "test"
    return app


# ---------------------------------------------------------------------------
# Shared mock data
# ---------------------------------------------------------------------------
MOCK_USER = {
    "userID": 1,
    "email": "jdoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "username": "jdoe",
    "available_funds": 1000.00,
}

MOCK_TRADE = {
    "stock_symbol": "AAPL",
    "number_of_shares": 5,
    "price": 150.00,
    "transaction_type": "BUY",
    "transaction_date": datetime(2026, 3, 1, 10, 0),
}

MOCK_SELL_TRADE = {
    "stock_symbol": "TSLA",
    "number_of_shares": -3,
    "price": 200.00,
    "transaction_type": "SELL",
    "transaction_date": datetime(2026, 3, 5, 14, 30),
}


def _make_cursor(users, rows):
    """Return a mock cursor whose fetchall alternates user -> trade rows."""
    cursor = MagicMock()
    cursor.fetchall.side_effect = [users, rows]
    cursor.nextset.return_value = False
    return cursor


def _make_db(cursor):
    db = MagicMock()
    db.cursor.return_value = cursor
    return db


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
class TestGenerateHistoryDownload(unittest.TestCase):

    def setUp(self):
        self.app = make_app()
        self.client = self.app.test_client()


    # ---------- response headers ----------

    @patch("routes.user_api.get_db")
    def test_response_mimetype_is_plain_text(self, mock_get_db):
        """Response Content-Type must be text/plain."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")

        self.assertIn("text/plain", resp.content_type)


    @patch("routes.user_api.get_db")
    def test_content_disposition_triggers_download(self, mock_get_db):
        """Content-Disposition must be an attachment with the right filename."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")

        disposition = resp.headers.get("Content-Disposition", "")
        self.assertIn("attachment", disposition)
        self.assertIn("trade_history_user_1.txt", disposition)


    @patch("routes.user_api.get_db")
    def test_status_code_200(self, mock_get_db):
        """Endpoint must return HTTP 200 for a valid user."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")

        self.assertEqual(resp.status_code, 200)


    # ---------- file header / metadata ----------

    @patch("routes.user_api.get_db")
    def test_file_contains_trade_history_title(self, mock_get_db):
        """Exported file must start with the TRADE HISTORY heading."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("TRADE HISTORY", body)


    @patch("routes.user_api.get_db")
    def test_file_contains_username(self, mock_get_db):
        """Exported file must include the user's username in the header."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("jdoe", body)


    @patch("routes.user_api.get_db")
    def test_file_contains_todays_date(self, mock_get_db):
        """Exported file header must include today's date (YYYY-MM-DD)."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        today = datetime.today().strftime("%Y-%m-%d")
        self.assertIn(today, body)


    @patch("routes.user_api.get_db")
    def test_file_contains_column_headers(self, mock_get_db):
        """Exported file must include the column header row."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        for col in ("Date", "Symbol", "Type", "Shares", "Price", "Total"):
            self.assertIn(col, body)


    # ---------- trade row content ----------

    @patch("routes.user_api.get_db")
    def test_trade_symbol_appears_in_output(self, mock_get_db):
        """Stock symbol from the trade must appear in the exported file."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("AAPL", body)


    @patch("routes.user_api.get_db")
    def test_trade_type_appears_in_output(self, mock_get_db):
        """Transaction type (BUY/SELL) must appear in the exported file."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("BUY", body)


    @patch("routes.user_api.get_db")
    def test_trade_price_appears_in_output(self, mock_get_db):
        """Trade price must appear formatted in the exported file."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("150.00", body)


    @patch("routes.user_api.get_db")
    def test_trade_total_is_correct(self, mock_get_db):
        """Total (shares x price) must be correct in the exported file."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        # 5 shares x $150.00 = $750.00
        self.assertIn("750.00", body)


    @patch("routes.user_api.get_db")
    def test_trade_date_appears_in_output(self, mock_get_db):
        """Transaction date must appear in the exported file."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("2026-03-01", body)


    @patch("routes.user_api.get_db")
    def test_negative_shares_rendered_as_absolute(self, mock_get_db):
        """SELL trades stored with negative share counts must show positive numbers."""
        cursor = _make_cursor([MOCK_USER], [MOCK_SELL_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("3", body)
        self.assertNotIn("-3", body)


    # ---------- empty history ----------

    @patch("routes.user_api.get_db")
    def test_empty_history_still_returns_200(self, mock_get_db):
        """A user with no trades must still get a valid 200 response."""
        cursor = _make_cursor([MOCK_USER], [])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")

        self.assertEqual(resp.status_code, 200)


    @patch("routes.user_api.get_db")
    def test_empty_history_file_has_header_but_no_rows(self, mock_get_db):
        """With no trades the file should have the header but no data rows."""
        cursor = _make_cursor([MOCK_USER], [])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("TRADE HISTORY", body)
        self.assertNotIn("AAPL", body)
        self.assertNotIn("TSLA", body)


    # ---------- multiple trades ----------

    @patch("routes.user_api.get_db")
    def test_multiple_trades_all_appear_in_output(self, mock_get_db):
        """All trades must appear when a user has more than one transaction."""
        cursor = _make_cursor([MOCK_USER], [MOCK_TRADE, MOCK_SELL_TRADE])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/1/generate-history-download")
        body = resp.data.decode()

        self.assertIn("AAPL", body)
        self.assertIn("TSLA", body)
        self.assertIn("BUY", body)
        self.assertIn("SELL", body)


    # ---------- filename uses correct user ID ----------

    @patch("routes.user_api.get_db")
    def test_filename_reflects_requested_user_id(self, mock_get_db):
        """Filename in Content-Disposition must use the requested user ID."""
        user = {**MOCK_USER, "userID": 42, "username": "user42"}
        cursor = _make_cursor([user], [])
        mock_get_db.return_value = _make_db(cursor)

        resp = self.client.get("/user/42/generate-history-download")

        disposition = resp.headers.get("Content-Disposition", "")
        self.assertIn("trade_history_user_42.txt", disposition)


if __name__ == "__main__":
    unittest.main(verbosity=2)
