
from passwordManager import SQLiteDB  


class UserInterface:
    def __init__(self, db, encryptor):
        """Initialize the UI with the database and encryptor classes."""
        self.db = db
        self.encryptor = encryptor

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

        encrypted_password = self.encryptor.encrypt(password)
        self.db.cursor.execute("INSERT INTO passwords (website_name, username, password) VALUES (?, ?, ?)",
                               (website, username, encrypted_password))
        self.db.connection.commit()
        print("Password added successfully!")

    def get_password(self):
        """Retrieves a password from the database."""
        website = input("Enter the webite name: ").strip()
        username = input("Enter the username: ").strip()

        if not website or not username:
            print("Both are required!")
            return

        self.db.cursor.execute("SELECT password FROM passwords WHERE website_name=? AND username=?", (website, username))
        result = self.db.cursor.fetchone()

        if result:
            decrypted_password = self.encryptor.decrypt(result[0])
            print(f"The password for {username} on {website} is: {decrypted_password}")
        else:
            print("No matching record found.")

    def delete_password(self):
        """Deletes a password from the database."""
        website = input("Enter the website name to delete: ").strip()
        username = input("Enter the username: ").strip()

        if not website or not username:
            print("Both website and username are required!")
            return

        self.db.cursor.execute("DELETE FROM passwords WHERE website_name=? AND username=?", (website, username))
        self.db.connection.commit()
        print("Password deleted successfully.")

    def list_passwords(self):
        """List all stored passwords."""
        self.db.cursor.execute("SELECT website_name, username FROM passwords")
        results = self.db.cursor.fetchall()

        if results:
            print("\nStored Passwords:")
            for website, username in results:
                print(f"Website: {website}, Username: {username}")
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
                break
            else:
                print("Invalid choice. Please try again.")
