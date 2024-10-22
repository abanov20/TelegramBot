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
                    comment TEXT
                    )
                """)

            connection.commit()

    def execute(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()


