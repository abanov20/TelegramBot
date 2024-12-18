import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_table(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS review (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone_number INTEGER,
                    visit_date DATETIME,
                    food_rating INTEGER,
                    cleanliness_rating INTEGER,
                    tg_id INTEGER,
                    comment TEXT
                    )
                """)

            connection.execute("""
            CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_food TEXT,
            price INTEGER,
            category_food TEXT
            )""")

            connection.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            first_name TEXT
            )""")

            connection.commit()

    def execute(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor


    def fetch(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as connect:
            result = connect.execute(query, params)
            result.row_factory = sqlite3.Row

            data = result.fetchall()
            return [dict(row) for row in data]