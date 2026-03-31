# """
# test_user_repository.py
# =======================
# Integration tests for LoginAPI and SignupAPI against the real
# user_test table on the creamcheesepeanutbutter AlwaysData database.

# Run:
#     python -m unittest test_user_repository -v
#     pytest test_user_repository.py -v
# """

# import unittest
# import mysql.connector

# # ── DB connection ─────────────────────────────────────────────────────────────

# DB_CONFIG = {
#     "host":     "mysql-creamcheesepeanutbutter.alwaysdata.net",
#     "user":     "creamcheesepeanutbutter_yusuf",
#     "password": "ilikepeanutbutter3",
#     "database": "creamcheesepeanutbutter_users",
# }

# TABLE = "user_test"


# def get_connection():
#     return mysql.connector.connect(**DB_CONFIG)


# # =============================================================================
# # Login tests
# # =============================================================================

# class TestLogin(unittest.TestCase):

#     def test_login_user_that_exists(self):
#         """Login with jdoe's real credentials should return exactly 1 row."""
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)

#         cursor.execute(
#             f"SELECT * FROM {TABLE} WHERE email = %s AND password = %s",
#             ("jdoe@example.com", "password123")
#         )
#         user = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         self.assertIsNotNone(user, "Expected to find jdoe but got nothing")
#         self.assertEqual(user["username"], "jdoe")

#     def test_login_user_that_does_not_exist(self):
#         """Login with a fake email should return no row."""
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)

#         cursor.execute(
#             f"SELECT * FROM {TABLE} WHERE email = %s AND password = %s",
#             ("ghost@nowhere.com", "fakepassword")
#         )
#         user = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         self.assertIsNone(user, "Expected no user but got a result")


# # =============================================================================
# # Signup tests
# # =============================================================================

# class TestSignup(unittest.TestCase):

#     TEST_EMAIL    = "testuser_lab8@example.com"
#     TEST_USERNAME = "testuser_lab8"
#     TEST_PASSWORD = "testpass123"

#     def tearDown(self):
#         """Clean up the test account after each signup test."""
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute(f"DELETE FROM {TABLE} WHERE email = %s", (self.TEST_EMAIL,))
#         conn.commit()
#         cursor.close()
#         conn.close()

#     def test_signup_user_that_does_not_exist(self):
#         """Inserting a brand new user should succeed with no errors."""
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(
#             f"INSERT INTO {TABLE} (username, password, email, first_name, last_name)"
#             f" VALUES (%s, %s, %s, %s, %s)",
#             (self.TEST_USERNAME, self.TEST_PASSWORD, self.TEST_EMAIL, "Test", "User")
#         )
#         conn.commit()

#         cursor.close()
#         conn.close()

#         self.assertEqual(cursor.rowcount, 1, "Expected 1 row to be inserted")

#     def test_signup_user_that_already_exists(self):
#         """Trying to insert a duplicate email should find the existing row first."""
#         # First insert the user
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             f"INSERT INTO {TABLE} (username, password, email, first_name, last_name)"
#             f" VALUES (%s, %s, %s, %s, %s)",
#             (self.TEST_USERNAME, self.TEST_PASSWORD, self.TEST_EMAIL, "Test", "User")
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         # Now try to register again with the same email
#         conn2 = get_connection()
#         cursor2 = conn2.cursor(dictionary=True)
#         cursor2.execute(
#             f"SELECT * FROM {TABLE} WHERE email = %s", (self.TEST_EMAIL,)
#         )
#         existing = cursor2.fetchone()
#         cursor2.close()
#         conn2.close()

#         self.assertIsNotNone(existing, "User should already exist — signup must be rejected")

#     def test_signup_then_verify_user_exists(self):
#         """After signing up, searching for the new account should find it."""
#         # Sign up
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             f"INSERT INTO {TABLE} (username, password, email, first_name, last_name)"
#             f" VALUES (%s, %s, %s, %s, %s)",
#             (self.TEST_USERNAME, self.TEST_PASSWORD, self.TEST_EMAIL, "Test", "User")
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         # Verify the account exists
#         conn2 = get_connection()
#         cursor2 = conn2.cursor(dictionary=True)
#         cursor2.execute(
#             f"SELECT * FROM {TABLE} WHERE email = %s", (self.TEST_EMAIL,)
#         )
#         user = cursor2.fetchone()
#         cursor2.close()
#         conn2.close()

#         self.assertIsNotNone(user, "Newly created user should be found in the database")
#         self.assertEqual(user["username"], self.TEST_USERNAME)
#         self.assertEqual(user["email"],    self.TEST_EMAIL)


# # =============================================================================
# # Entry point
# # =============================================================================

# if __name__ == "__main__":
#     unittest.main(verbosity=2)