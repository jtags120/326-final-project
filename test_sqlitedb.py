# type "python3 test_sqlitedb.py" for the unit test run. It should say "Ran 5 tests in "under 1 second" " 

import unittest
import sqlite3
import pandas as pd

# -------------------------- SQLite Database Class ---------------------
class SQLiteDB:
    def __init__(self, db_file="passwords.db"):
        """
        Initializes the SQLiteDB instance, connecting to the specified database file.
        """
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """
        Creates the table for storing passwords if it doesn't already exist.
        """
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def store_password(self, website_name, username, password):
        """
        Stores the password in the database.
        """
        insert_query = '''
        INSERT INTO passwords (website_name, username, password)
        VALUES (?, ?, ?)
        '''
        self.cursor.execute(insert_query, (website_name, username, password))
        self.connection.commit()

    def get_password(self, website_name, username):
        """
        Retrieves the password from the database.
        """
        select_query = '''
        SELECT password FROM passwords
        WHERE website_name = ? AND username = ?
        '''
        self.cursor.execute(select_query, (website_name, username))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_password(self, website_name, username):
        """
        Deletes the password from the database.
        """
        delete_query = '''
        DELETE FROM passwords
        WHERE website_name = ? AND username = ?
        '''
        self.cursor.execute(delete_query, (website_name, username))
        self.connection.commit()

    def list_passwords(self):
        """
        Lists all the passwords in the database.
        """
        select_all_query = '''
        SELECT website_name, username, password FROM passwords
        '''
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=['website_name', 'username', 'password'])

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()

# -------------------------- Unit Test Class ---------------------------
class TestSQLiteDB(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary database for testing."""
        self.db = SQLiteDB("test_passwords.db")
    
    def tearDown(self):
        """Clean up after each test."""
        self.db.close()
        import os
        os.remove("test_passwords.db")
    
    def test_create_table(self):
        """Test table creation."""
        self.db._create_table()
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
        table_exists = self.db.cursor.fetchone()
        self.assertIsNotNone(table_exists, "Table 'passwords' should exist.")
    
    def test_store_password(self):
        """Test storing a password."""
        self.db.store_password("example.com", "test_user", "test_password")
        self.db.cursor.execute("SELECT * FROM passwords WHERE website_name=? AND username=?", ("example.com", "test_user"))
        row = self.db.cursor.fetchone()
        self.assertIsNotNone(row, "Password should be stored in the database.")
        self.assertEqual(row[2], "test_user")
        self.assertEqual(row[3], "test_password")
    
    def test_get_password(self):
        """Test retrieving a password."""
        self.db.store_password("example.com", "test_user", "test_password")
        password = self.db.get_password("example.com", "test_user")
        self.assertEqual(password, "test_password", "Retrieved password should match stored password.")
    
    def test_delete_password(self):
        """Test deleting a password."""
        self.db.store_password("example.com", "test_user", "test_password")
        self.db.delete_password("example.com", "test_user")
        password = self.db.get_password("example.com", "test_user")
        self.assertIsNone(password, "Password should be deleted from the database.")
    
    def test_list_passwords(self):
        """Test listing all passwords."""
        self.db.store_password("example.com", "test_user", "test_password")
        self.db.store_password("another.com", "user2", "password2")
        df = self.db.list_passwords()
        self.assertEqual(len(df), 2, "There should be two entries in the database.")
        self.assertIn("example.com", df['website_name'].values)
        self.assertIn("another.com", df['website_name'].values)

if __name__ == "__main__":
    unittest.main()
