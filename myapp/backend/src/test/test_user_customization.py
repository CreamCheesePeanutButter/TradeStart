"""
test_change_user_api.py
=======================
Tests for intentionally broken ChangeUsernameAPI and ChangePasswordAPI

Uses same DB config as test_user_repository.py
"""

import unittest
import mysql.connector

# ── DB connection (same config) ─────────────────────────────

DB_CONFIG = {
    "host":     "mysql-creamcheesepeanutbutter.alwaysdata.net",
    "user":     "creamcheesepeanutbutter_yusuf",
    "password": "ilikepeanutbutter3",
    "database": "creamcheesepeanutbutter_users",
}

TABLE = "test_user"


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# USERNAME TESTS
# ============================================================

class TestChangeUsername(unittest.TestCase):

    USER_ID = 1


    def test_change_username_OB(self):
        """
        UT-06-OB
        Opaque Box:
        Only simulate update query execution
        """

        conn = get_connection()
        cursor = conn.cursor()

        # simulate API behavior
        cursor.execute(
            """
            UPDATE test_user
            SET user_name = %s
            WHERE id = %s
            """,
            (self.USER_ID, "newname")  # wrong order
        )

        conn.commit()

        cursor.close()
        conn.close()

        self.assertTrue(True)   # only checks execution


    def test_change_username_TB(self):
        """
        UT-07-TB
        Translucent Box:
        Verify username should change but will fail
        because column name is incorrect
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE test_user
            SET user_name = %s
            WHERE id = %s
            """,
            (self.USER_ID, "newname")
        )

        conn.commit()

        cursor.close()
        conn.close()


        # check real username column
        conn2 = get_connection()
        cursor2 = conn2.cursor(dictionary=True)

        cursor2.execute(
            f"SELECT username FROM {TABLE} WHERE id = %s",
            (self.USER_ID,)
        )

        user = cursor2.fetchone()

        cursor2.close()
        conn2.close()

        # should fail because username not updated
        self.assertEqual(user["username"], "newname")


    def test_change_username_CB(self):
        """
        UT-08-CB
        Clear Box:
        We know wrong column name is used (user_name)
        so username column should remain unchanged
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE test_user
            SET user_name = %s
            WHERE id = %s
            """,
            (self.USER_ID, "wrongtest")
        )

        conn.commit()

        cursor.close()
        conn.close()


        conn2 = get_connection()
        cursor2 = conn2.cursor(dictionary=True)

        cursor2.execute(
            f"SELECT username FROM {TABLE} WHERE id = %s",
            (self.USER_ID,)
        )

        user = cursor2.fetchone()

        cursor2.close()
        conn2.close()

        self.assertNotEqual(user["username"], "wrongtest")



# ============================================================
# PASSWORD TESTS
# ============================================================

class TestChangePassword(unittest.TestCase):

    USER_ID = 1


    def test_change_password_OB(self):
        """
        UT-09-OB
        Opaque Box:
        Query executes successfully
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE test_user
            SET password = %s
            """,
            ("123456",)
        )

        conn.commit()

        cursor.close()
        conn.close()

        self.assertTrue(True)


    def test_change_password_CB(self):
        """
        UT-10-CB
        Clear Box:
        Missing WHERE clause updates ALL users
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE test_user
            SET password = %s
            """,
            ("globalpass",)
        )

        conn.commit()

        cursor.close()
        conn.close()


        conn2 = get_connection()
        cursor2 = conn2.cursor(dictionary=True)

        cursor2.execute(
            "SELECT password FROM test_user LIMIT 2"
        )

        users = cursor2.fetchall()

        cursor2.close()
        conn2.close()

        # all returned users will have same password (bug)
        self.assertEqual(users[0]["password"], "globalpass")
        self.assertEqual(users[1]["password"], "globalpass")


    def test_change_password_TB(self):
        """
        UT-11-TB
        Translucent Box:
        Expect only one user password to change
        but bug updates entire table
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE test_user
            SET password = %s
            """,
            ("mypassword",)
        )

        conn.commit()

        cursor.close()
        conn.close()


        conn2 = get_connection()
        cursor2 = conn2.cursor(dictionary=True)

        cursor2.execute(
            f"SELECT password FROM {TABLE} WHERE id = %s",
            (self.USER_ID,)
        )

        user = cursor2.fetchone()

        cursor2.close()
        conn2.close()

        self.assertEqual(user["password"], "mypassword")



# ============================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)