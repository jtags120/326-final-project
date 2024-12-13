import sqlite3
import pandas as pd
from cryptography.fernet import Fernet
import getpass
import os


# ------------------------- Authentication Class -------------------------
class UserAuthentication:
    def __init__(self):
        """Constructor for UserAuthentication."""
        self.stored_username = "admin"
        self.stored_password =  "password"  

    def authenticate(self) -> bool:
        for i in range(3):
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            if username == self.stored_username and password == self.stored_password:
                return True
            print("Authentication failed.")
        return False



# ------------------------ Encryptor Class ------------------------------
class Encryptor:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.fernet = Fernet(self.key)
        
    def encrypt(self, plaintext: str) -> bytes:
        try:
            if not isinstance(plaintext, bytes):
                plaintext = plaintext.encode()
            enc_pass = self.fernet.encrypt(plaintext)
            return enc_pass
        except Exception as e:
            print(f"Error encrypting password: {type(e).__name__}")
            return None

    def decrypt(self, encrypted_text: bytes) -> str:
        try:
            dec_pass = self.fernet.decrypt(encrypted_text)
            return dec_pass.decode()
        except Exception as e:
            print(f"Error decrypting password: {type(e).__name__}")
            return None

# Ensure the rest of the class methods align with this change

# -------------------------- SQLite Database Class ---------------------
# Bryant Morris
# -------------------------- SQLite Database Class --------------------- 
# Update SQLiteDB class to accept an encryptor instance
class SQLiteDB:
    def __init__(self, db_file="passwords.db", encryptor=None):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_table()
        self.encryptor = encryptor if encryptor else Encryptor()
    
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
        password = self.encryptor.encrypt(password)
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
        if result:
            return self.encryptor.decrypt(result[0])
        return None


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
        df = pd.DataFrame(rows, columns=['website_name', 'username', 'password'])
        for i, password in enumerate(df['password'].values):
            enc_password = self.encryptor.decrypt(password)
            df.iloc[i, df.columns.get_loc('password')] = enc_password
        
        return df

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()
        
# -------------------------- User Interface Class -----------------------
class UserInterface:
    def __init__(self):
        """Initialize the UI with the database and encryptor classes."""
        self.db = SQLiteDB()

    def display_menu(self):
        """Display the menu options for the user."""
        print("\nPassword Manager Menu:")
        print("1. Add a Password")
        print("2. Retrieve a Password")
        print("3. Delete a Password")
        print("4. List All Passwords")
        print("5. Leave")

    def add_password(self):
        """Add a new password to the database."""
        website = input("Enter the website name: ").strip()
        username = input("Enter the username: ").strip()
        password = input("Enter the password: ").strip()

        if not website or not username or not password:
            print("All fields are required!")
            return

        self.db.store_password(website, username, password)
        print("Password added successfully!")

    def get_password(self):
        """Retrieves a password from the database."""
        website = input("Enter the webite name: ").strip()
        username = input("Enter the username: ").strip()

        if not website or not username:
            print("Both are required!")
            return

        result = self.db.get_password(website, username)

        if result:
            print(f"The password for {username} on {website} is: {result}")
        else:
            print("No matching record found.")

    def delete_password(self):
        """Deletes a password from the database."""
        website = input("Enter the website name to delete: ").strip()
        username = input("Enter the username: ").strip()

        if not website or not username:
            print("Both website and username are required!")
            return

        self.db.delete_password(website, username)
        print("Password deleted successfully.")

    def list_passwords(self):
        """List all stored passwords."""
        
        results = self.db.list_passwords()

        if not results.empty:
            print("\nStored Passwords:")
            for index, row in results.iterrows():
                print(f"Website: {row['website_name']}, Username: {row['username']}, Password: {row['password']}")
        else:
            print("No passwords stored.")

    def run(self):
        """Run the min menu and handle user inputs."""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_password()
            elif choice == "2":
                self.get_password()
            elif choice == "3":
                self.delete_password()
            elif choice == "4":
                self.list_passwords()
            elif choice == "5":
                print("Exiting Password Manager. Goodbye!")
                self.db.close()
                break
            else:
                print("Invalid choice. Please try again.")


# ------------------------ Main Program Logic ---------------------------

def main():
    
    ua = UserAuthentication()
    if(ua.authenticate()):
        ui = UserInterface()
        ui.run()
    
    os.remove("passwords.db")


if __name__ == "__main__":
    main()
