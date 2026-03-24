from db import get_db
class Trade:
    def __init__(self, ticker, price, quantity, time):
        self.ticker = ticker
        self.price = price #price at that time
        self.quantity = quantity
        self.time = time

class TradeHistory:
    _trades = []

    def __init__(self, userID):
        self._trades = []
        self.loadTrades(userID)

    def loadTrades(self, userID):
        db = get_db()

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM TradeTable WHERE userID = %s", (userID,))
        trades_data = cursor.fetchall()

        # Iterate through the results and create Trade objects
        for row in trades_data:
            # We map the database column names to the Trade class parameters
            # Note: Ensure 'price' exists in your TradeTable schema
            trade_obj = Trade(
                ticker=row['stock_symbol'],
                price=row.get('price', 0),  # Using .get() in case price isn't in the DB yet
                quantity=row['number_of_shares'],
                time=row['transaction_date']
            )
            self._trades.append(trade_obj)
            
        cursor.close() 


    def add_trade(self, trade):
        self._trades.append(trade)
    
    def get_trades(self):
        return self._trades