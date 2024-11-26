import sqlite3
import pandas as pd
from cryptography.fernet import Fernet
import getpass


# ------------------------- Authentication Class -------------------------
class UserAuthentication:
    def __init__(self):
        """Constructor for UserAuthentication."""
        pass

    def authenticate(self) -> bool:
        '''Authenticates the user
        Returns:
            True if the user is authenticated, False otherwise
        '''
        pass


# ------------------------ Encryptor Class ------------------------------
class Encryptor:
    def __init__(self, key):
        if(key == None):
            self.key = Fernet.generate_key()
        else:
            pass
        self.fernet = Fernet(self.key)
        

    def encrypt(self, plaintext: str) -> str:
        '''Encrypts the plaintext passwords
        
        Args:
            plaintext (str): The plaintext password to encrypt
        Returns:
            str: The encrypted password
        '''
        enc_pass = self.fernet.encrypt(plaintext.encode())
        return enc_pass

    def decrypt(self, encrypted_text: str) -> str:
        '''Decrypts the encrypted passwords
        
        Args:
            encrypted_text (str): The encrypted password to decrypt
        Returns:
            str: The decrypted password
        '''
        dec_pass = self.fernet.decrypt(encrypted_text).decode()
        return dec_pass


# -------------------------- SQLite Database Class ---------------------
# Bryant Morris
# -------------------------- SQLite Database Class ---------------------

class SQLiteDB:
    def __init__(self, db_file="passwords.db"):
        """
        Initializes the SQLiteDB instance, connecting to the specified database file.

        Args:
            db_file (str): The database file name.
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
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def store_password(self, username, encrypted_password):
        """
        Stores the password in the database.

        Args:
            username (str): The username of the user.
            encrypted_password (str): The encrypted password.
        """
        insert_query = '''
        INSERT INTO passwords (username, encrypted_password)
        VALUES (?, ?)
        '''
        self.cursor.execute(insert_query, (username, encrypted_password))
        self.connection.commit()

    def get_password(self, username):
        """
        Retrieves the password from the database.

        Args:
            username (str): The username of the user.

        Returns:
            str: The encrypted password, or None if not found.
        """
        select_query = '''
        SELECT encrypted_password FROM passwords
        WHERE username = ?
        '''
        self.cursor.execute(select_query, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_password(self, username):
        """
        Deletes the password from the database.

        Args:
            username (str): The username of the user.
        """
        delete_query = '''
        DELETE FROM passwords
        WHERE username = ?
        '''
        self.cursor.execute(delete_query, (username,))
        self.connection.commit()

    def list_passwords(self):
        """
        Lists all the passwords in the database.

        Returns:
            pd.DataFrame: A DataFrame containing all the passwords.
        """
        select_all_query = '''
        SELECT username, encrypted_password FROM passwords
        '''
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=['username', 'encrypted_password'])

# -------------------------- User Interface Class -----------------------
class UserInterface:
    def __init__(self):
        """Constructor for the User Interface."""
        pass

    def add_password(self, encryptor: Encryptor, db: SQLiteDB):
        '''Adds a new password to the database
        
        Args:
            encryptor (Encryptor): The encryptor object
            db (SQLiteDB): The database object'''
        pass

    def get_password(self, encryptor: Encryptor, db: SQLiteDB):
        '''Retrieves the password from the database
        
        Args:
            encryptor (Encryptor): The encryptor object
            db (SQLiteDB): The database object
        Returns:
            str: The decrypted password
        '''
        pass

    def delete_password(self, db: SQLiteDB):
        '''Deletes the password from the database
        
        Args:
            db (SQLiteDB): The database object'''
        pass

    def list_passwords(self, db: SQLiteDB):
        '''Lists all the passwords in the database
        
        Args:
            db (SQLiteDB): The database object'''
        pass


# ------------------------ Main Program Logic ---------------------------

def main():
    pass
    


if __name__ == "__main__":
    main()
