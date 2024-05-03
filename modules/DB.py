import mysql.connector

class DatabaseHandler:
    def __init__(self, config):
        self.config = config
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)

    def query_db(self, query, args=None, one=False):
        self.cursor.execute(query, args or ())
        result = self.cursor.fetchall()
        return (result[0] if result else None) if one else result

    def close(self):
        self.cursor.close()
        self.connection.close()

# Toda esta clase es para hacer la conexión y los querys