"""
test_user_repository.py
=======================
Unit tests for LoginAPI and SignupAPI — the two existing route classes
in the creamcheesepeanutbutter backend.

Classes under test
------------------
  LoginAPI  (routes/login_api.py)  — post()
  SignupAPI (routes/signup_api.py) — post()

How it works
------------
* Flask's built-in test client sends fake HTTP requests; no live server needed.
* unittest.mock.patch replaces `get_db` with a MagicMock — no real DB calls.
* flask_cors, mysql.connector, and the stock tracker (which calls an external
  API at import time) are all stubbed so tests run with zero network access.

Run:
    python -m unittest test_user_repository -v
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch
import os


_cors = types.ModuleType("flask_cors")
_cors.CORS = lambda app, **kw: None
sys.modules.setdefault("flask_cors", _cors)


_mysql_pkg = types.ModuleType("mysql")
_mysql_con = types.ModuleType("mysql.connector")
_mysql_pkg.connector = _mysql_con
sys.modules.setdefault("mysql", _mysql_pkg)
sys.modules.setdefault("mysql.connector", _mysql_con)


_tracker_mod = types.ModuleType("tracker.stock_tracker")
_tracker_mod.StockTracker = MagicMock
_tracker_parent = types.ModuleType("tracker")
_tracker_parent.stock_tracker = _tracker_mod
sys.modules.setdefault("tracker", _tracker_parent)
sys.modules.setdefault("tracker.stock_tracker", _tracker_mod)


SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..")
sys.path.insert(0, SRC)

from app import app  # noqa: E402


SAMPLE_USER = {
    "userID": 1,
    "username": "jdoe",
    "password": "password123",
    "email": "jdoe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "admin_access": 0,
    "available_funds": 0,
}


def make_mock_db(fetchone_return=None):
    """Return (mock_connection, mock_cursor) wired for tests."""
    cursor = MagicMock()
    cursor.fetchone.return_value = fetchone_return
    db = MagicMock()
    db.cursor.return_value = cursor
    return db, cursor


# Class 1 — LoginAPI   POST /login

class TestLoginAPIPost(unittest.TestCase):
    """Tests for LoginAPI.post()"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # happy path ──────────────────────────────────────────────────────────────

    def test_valid_credentials_return_200(self):
        """Correct email + password → 200 Login successful."""
        mock_db, _ = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "jdoe@example.com",
                                       "password": "password123"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["message"], "Login successful")

    def test_valid_login_returns_full_user_object(self):
        """Response body must include the user dict returned by the DB."""
        mock_db, _ = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "jdoe@example.com",
                                       "password": "password123"})
        user = r.get_json()["user"]
        self.assertEqual(user["userID"], 1)
        self.assertEqual(user["email"], "jdoe@example.com")

    def test_numeric_password_authenticates_correctly(self):
        """'peanutbutter' uses the purely numeric password '123456789'."""
        pb = {**SAMPLE_USER, "username": "peanutbutter",
              "email": "kanle2k6@gmail.com", "password": "123456789"}
        mock_db, _ = make_mock_db(fetchone_return=pb)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "kanle2k6@gmail.com",
                                       "password": "123456789"})
        self.assertEqual(r.status_code, 200)

    # wrong credentials ───────────────────────────────────────────────────────

    def test_wrong_password_returns_401(self):
        """Mismatched password → 401 Invalid credentials."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "jdoe@example.com",
                                       "password": "WRONG"})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.get_json()["message"], "Invalid credentials")

    def test_wrong_email_returns_401(self):
        """Unknown email → 401."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "nobody@nowhere.com",
                                       "password": "password123"})
        self.assertEqual(r.status_code, 401)

    def test_cross_user_password_is_rejected(self):
        """
        Alice's password ('testpass') used against Bob's email must fail.
        The DB returns None because the email+password pair won't match.
        """
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "bjohnson@example.com",
                                       "password": "testpass"})
        self.assertEqual(r.status_code, 401,
                         "Cross-user password reuse must be rejected")

    def test_admin_password_cannot_log_in_regular_user(self):
        """'adminpass' must not authenticate a non-admin account."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.login_api.get_db", return_value=mock_db):
            r = self.client.post("/login",
                                 json={"email": "mlee@example.com",
                                       "password": "adminpass"})
        self.assertEqual(r.status_code, 401)

    # missing / empty fields ──────────────────────────────────────────────────

    def test_missing_password_returns_400(self):
        """No password key → 400 Missing email or password."""
        r = self.client.post("/login", json={"email": "jdoe@example.com"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("Missing", r.get_json()["message"])

    def test_missing_email_returns_400(self):
        """No email key → 400."""
        r = self.client.post("/login", json={"password": "password123"})
        self.assertEqual(r.status_code, 400)

    def test_empty_password_string_returns_400(self):
        """Empty-string password is falsy → treated as missing."""
        r = self.client.post("/login",
                             json={"email": "jdoe@example.com", "password": ""})
        self.assertEqual(r.status_code, 400)

    def test_empty_email_string_returns_400(self):
        """Empty-string email is falsy → 400."""
        r = self.client.post("/login",
                             json={"email": "", "password": "password123"})
        self.assertEqual(r.status_code, 400)

    def test_completely_empty_body_returns_400(self):
        """JSON body with no fields at all → 400."""
        r = self.client.post("/login", json={})
        self.assertEqual(r.status_code, 400)

    # DB interaction ──────────────────────────────────────────────────────────

    def test_query_uses_parameterised_values(self):
        """SQL injection safety: cursor must receive %s placeholders + a tuple."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        injection = "' OR '1'='1"
        with patch("routes.login_api.get_db", return_value=mock_db):
            self.client.post("/login",
                             json={"email": "jdoe@example.com",
                                   "password": injection})
        sql, params = mock_cursor.execute.call_args[0]
        self.assertIn("%s", sql)
        self.assertIn(injection, params)

    def test_cursor_closed_after_successful_login(self):
        """cursor.close() must be called to prevent connection leaks."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.login_api.get_db", return_value=mock_db):
            self.client.post("/login",
                             json={"email": "jdoe@example.com",
                                   "password": "password123"})
        mock_cursor.close.assert_called_once()

    def test_cursor_closed_after_failed_login(self):
        """cursor.close() must be called even when credentials are wrong."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.login_api.get_db", return_value=mock_db):
            self.client.post("/login",
                             json={"email": "jdoe@example.com",
                                   "password": "WRONG"})
        mock_cursor.close.assert_called_once()


# =============================================================================
# Class 2 — SignupAPI   POST /signup
# =============================================================================

class TestSignupAPIPost(unittest.TestCase):
    """Tests for SignupAPI.post()"""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # happy path ──────────────────────────────────────────────────────────────

    def test_new_user_returns_201(self):
        """Fresh email + password → 201 User registered successfully."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            r = self.client.post("/signup",
                                 json={"email": "newuser@example.com",
                                       "password": "securepass",
                                       "username": "newuser",
                                       "first_name": "New",
                                       "last_name": "User"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["message"], "User registered successfully")

    def test_signup_commits_to_database(self):
        """A successful registration must call db.commit()."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "commit@example.com",
                                   "password": "pass"})
        mock_db.commit.assert_called_once()

    def test_optional_fields_default_to_empty_string(self):
        """first_name, last_name, username are optional — omitting them is fine."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            r = self.client.post("/signup",
                                 json={"email": "minimal@example.com",
                                       "password": "minpass"})
        self.assertEqual(r.status_code, 201)
        sql, params = mock_cursor.execute.call_args_list[-1][0]
        self.assertEqual(params[2], "")  # first_name
        self.assertEqual(params[3], "")  # last_name
        self.assertEqual(params[4], "")  # username

    # duplicate email ─────────────────────────────────────────────────────────

    def test_duplicate_email_returns_409(self):
        """Existing email → 409 User already exists."""
        mock_db, _ = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            r = self.client.post("/signup",
                                 json={"email": "jdoe@example.com",
                                       "password": "anypass"})
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.get_json()["message"], "User already exists")

    def test_no_insert_runs_on_duplicate_email(self):
        """When a duplicate is found, no INSERT should execute."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "jdoe@example.com",
                                   "password": "anypass"})
        for c in mock_cursor.execute.call_args_list:
            self.assertNotIn("INSERT", c[0][0].upper())

    # missing / empty fields ──────────────────────────────────────────────────

    def test_missing_email_returns_400(self):
        """No email → 400 Missing email or password."""
        r = self.client.post("/signup", json={"password": "pass"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("Missing", r.get_json()["message"])

    def test_missing_password_returns_400(self):
        """No password → 400."""
        r = self.client.post("/signup", json={"email": "a@b.com"})
        self.assertEqual(r.status_code, 400)

    def test_empty_email_returns_400(self):
        """Empty-string email is falsy → 400."""
        r = self.client.post("/signup",
                             json={"email": "", "password": "pass"})
        self.assertEqual(r.status_code, 400)

    def test_empty_password_returns_400(self):
        """Empty-string password is falsy → 400."""
        r = self.client.post("/signup",
                             json={"email": "a@b.com", "password": ""})
        self.assertEqual(r.status_code, 400)

    # password edge cases ─────────────────────────────────────────────────────

    def test_numeric_password_is_stored(self):
        """Purely numeric passwords like '123456789' must be stored as-is."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            r = self.client.post("/signup",
                                 json={"email": "numericpw@example.com",
                                       "password": "123456789"})
        self.assertEqual(r.status_code, 201)
        sql, params = mock_cursor.execute.call_args_list[-1][0]
        self.assertIn("123456789", params)

    def test_special_character_password_is_stored(self):
        """Passwords with symbols like 'P@$$w0rd!' must be accepted verbatim."""
        mock_db, _ = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            r = self.client.post("/signup",
                                 json={"email": "special@example.com",
                                       "password": "P@$$w0rd!"})
        self.assertEqual(r.status_code, 201)

    def test_password_stored_in_plaintext(self):
        """
        KNOWN ISSUE — passwords are stored in plaintext.
        This test documents the current behaviour; it should FAIL
        once password hashing is added in a future iteration.
        """
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "plaintext@example.com",
                                   "password": "mypassword"})
        sql, params = mock_cursor.execute.call_args_list[-1][0]
        self.assertIn("mypassword", params)

    # DB interaction ──────────────────────────────────────────────────────────

    def test_cursor_closed_after_successful_signup(self):
        """cursor.close() must be called on success."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "closetest@example.com",
                                   "password": "pass"})
        mock_cursor.close.assert_called()

    def test_cursor_closed_after_duplicate_rejection(self):
        """cursor.close() must be called even when a duplicate is detected."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=SAMPLE_USER)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "jdoe@example.com",
                                   "password": "anypass"})
        mock_cursor.close.assert_called()

    def test_insert_uses_parameterised_query(self):
        """INSERT must use %s placeholders — not f-strings or % formatting."""
        mock_db, mock_cursor = make_mock_db(fetchone_return=None)
        with patch("routes.signup_api.get_db", return_value=mock_db):
            self.client.post("/signup",
                             json={"email": "paramtest@example.com",
                                   "password": "pass"})
        sql, params = mock_cursor.execute.call_args_list[-1][0]
        self.assertIn("%s", sql)


if __name__ == "__main__":
    unittest.main(verbosity=2)
