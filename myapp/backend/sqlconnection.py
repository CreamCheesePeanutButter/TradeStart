import mysql.connector
from mysql.connector import Error
class DatabaseConfig:
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.create_connection(self.host, self.user, self.password, self.database)
    
    def create_connection(self, host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection
    
    def get_users(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        return result
    def add_user(self, name, age, email):
        cursor = self.connection.cursor()
        query = "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)"
        values = (name, age, email)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

