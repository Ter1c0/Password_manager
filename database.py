import sqlite3
# Database class to handle SQLite interactions
class Database:
    def __init__(self):
        # Establish connection to the database file
        self.connection = sqlite3.connect("data.db")
        # Create tables if they do not exist
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userId TEXT PRIMARY KEY,
                registered_at TEXT NOT NULL
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                website TEXT NOT NULL,
                password TEXT NOT NULL,
                url1 TEXT,
                FOREIGN KEY (userId) REFERENCES users (userId)
            )
            """
        )
        self.connection.commit()

    # Execute a query with optional parameters
    def execute(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor

    # Commit the current transaction
    def commit(self):
        self.connection.commit()

    # Close the database connection
    def close(self):
        self.connection.close()
