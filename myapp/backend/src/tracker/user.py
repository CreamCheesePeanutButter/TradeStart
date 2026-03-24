from tracker.trade import TradeHistory, Trade
from datetime import datetime
from db import get_db


class User:

    def __init__(self, userID, l_name, f_name, free_fund, invested_fund=0):
        self._id = userID
        self._l_name = l_name
        self._f_name = f_name
        self._free_fund = free_fund
        self._invested_fund = invested_fund
        self._history_trade = TradeHistory(userID)

    def to_dict(self):
        return {
            "userID": self._id,
            "l_name": self._l_name,
            "f_name": self._f_name,
            "available_fund": self._free_fund,
            "invested_fund": self._invested_fund
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["userID"],
            data["last_name"],
            data["first_name"],
            data["available_funds"],
            data.get("invested_funds", 0)
        )

    # BUY
    def buy(self, num_stock, price, stock_key):

        pay_amount = num_stock * price

        if self._free_fund < pay_amount:
            return False

        self._free_fund -= float(pay_amount)
        self._invested_fund += float(pay_amount)

        db = get_db()
        cursor = db.cursor()

        try:

            cursor.execute(
                """
                UPDATE user
                SET available_funds = %s,
                    invested_funds = %s
                WHERE userID = %s
                """,
                (self._free_fund, self._invested_fund, self._id)
            )

            cursor.execute(
                """
                INSERT INTO TradeTable
                (userID, stock_symbol, number_of_shares, price, transaction_date, transaction_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    self._id,
                    stock_key,
                    num_stock,
                    price,
                    datetime.now(),
                    "BUY"
                )
            )

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(e)
            return False

        finally:
            cursor.close()

    # SELL
    def sell(self, num_stock, price, stock_key):

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT SUM(number_of_shares) as total_shares
            FROM TradeTable
            WHERE userID = %s AND stock_symbol = %s
            """,
            (self._id, stock_key)
        )

        result = cursor.fetchone()

        owned_shares = result["total_shares"] if result["total_shares"] else 0

        if owned_shares < num_stock:
            return False

        receive_amount = num_stock * price

        self._free_fund += float(receive_amount)
        self._invested_fund -= float(receive_amount)

        try:

            cursor.execute(
                """
                UPDATE user
                SET available_funds = %s,
                    invested_funds = %s
                WHERE userID = %s
                """,
                (self._free_fund, self._invested_fund, self._id)
            )

            cursor.execute(
                """
                INSERT INTO TradeTable
                (userID, stock_symbol, number_of_shares, price, transaction_date, transaction_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    self._id,
                    stock_key,
                    -num_stock,
                    price,
                    datetime.now(),
                    "SELL"
                )
            )

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            print(e)
            return False

        finally:
            cursor.close()