import pytest
import passwordManager as pm
from unittest.mock import patch
from cryptography.fernet import Fernet

def test_encrypt():
    '''Tests will test encrypting and decrypting passwords, including empty passwords,
    incorrect keys, or multiple encryption levels'''
    # Single encryption
    encryptor = pm.Encryptor()
    enc = encryptor.encrypt("password")
    assert encryptor.decrypt(enc) == "password"

    # Double encryption
    encryptor2 = pm.Encryptor()
    doubleEnc = encryptor2.encrypt(enc)
    assert encryptor.decrypt(encryptor2.decrypt(doubleEnc)) == "password"

    # Empty password
    emptyEnc = encryptor.encrypt("")
    assert encryptor.decrypt(emptyEnc) == ""

    # Incorrect key
    encryptor3 = pm.Encryptor()
    incorrectEnc = encryptor3.encrypt("password")
    assert encryptor.decrypt(incorrectEnc) != "password"

    # Non-letter character(nlc)
    nlc = encryptor.encrypt("test_password")
    assert encryptor.decrypt(nlc) == "test_password"

def test_db():
    '''Tests will test database creation, insertion, and deletion
    Edge case would be empty database'''

    # Create a single Encryptor for consistent encryption and decryption
    common_key = Fernet.generate_key()
    common_encryptor = pm.Encryptor(common_key)

    # Set up a temporary database for testing with the same Encryptor
    db = pm.SQLiteDB("test_passwords.db", encryptor=common_encryptor)

    try:
        # Test table creation.
        db._create_table()
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
        table_exists = db.cursor.fetchone()
        assert table_exists is not None, "Table 'passwords' should exist."

        # Test storing a password.
        db.store_password("example.com", "test_user", "test_password")
        db.cursor.execute("SELECT * FROM passwords WHERE website_name=? AND username=?", ("example.com", "test_user"))
        row = db.cursor.fetchone()
        print(f"Stored Row: {row}")  # Debugging statement
        decrypted_password = db.encryptor.decrypt(row[3])
        assert row is not None, "Password should be stored in the database."
        assert row[1] == "example.com"
        assert row[2] == "test_user"
        assert decrypted_password == "test_password"

        # Test retrieving a password.
        password = db.get_password("example.com", "test_user")
        print(f"Retrieved Password: {password}")  # Debugging statement
        assert password == "test_password", "Retrieved password should match stored password."

        # Test deleting a password.
        db.delete_password("example.com", "test_user")
        db.cursor.execute("SELECT * FROM passwords WHERE website_name=? AND username=?", ("example.com", "test_user"))
        row_after_delete = db.cursor.fetchone()
        print(f"Row after delete: {row_after_delete}")  # Debugging statement
        password = db.get_password("example.com", "test_user")
        print(f"Password after delete: {password}")  # Debugging statement
        assert password is None, "Password should be deleted from the database."

        # Test listing all passwords.
        db.store_password("example.com", "test_user", "test_password")
        db.store_password("another.com", "user2", "password2")
        df = db.list_passwords()
        assert len(df) == 2, "There should be two entries in the database."
        assert "example.com" in df['website_name'].values
        assert "another.com" in df['website_name'].values

    finally:
        # Clean up after each test.
        db.close()
        import os
        os.remove("test_passwords.db")

def test_auth():
    '''Tests will test logins, i.e. passworæd and username are correct inc. if
    password is empty'''
    # Simulate correct login
    auth = pm.UserAuthentication()
    with patch('builtins.input', return_value='admin'), patch('getpass.getpass', return_value='password'):
        assert auth.authenticate() == True
    # Simulate wrong login
    with patch('builtins.input', return_value='admin'), patch('getpass.getpass', return_value='wrong_password'):
        assert auth.authenticate() == False

def test_ui():
    '''Tests will test the user interface, i.e. command line'''
    #Test the correct option
    with patch('builtins.input', return_value='1'): 
        ui = pm.UserInterface()
        with patch.object(ui, 'add_password') as mock_add_password:
            ui.run() # Runs the UIloop
            mock_add_password.assert_called_once()

    # Tests invalid option 
    with patch('builtins.input', return_value='999'):
        ui = pm.UserInterface()
        with patch('builtins.print') as mock_print:
            ui.run()
            mock_print.assert_called_with("Invalid choice. Please try again.")

    # Test list of password options 
    with patch('builtins.input', return_value='4'):
        ui = pm.UserInterface()
        with patch.object(ui,'list_passwords') as mock_list_passwords:
            ui.run()
            mock_list_passwords.assert_called_once()



if __name__ == "__main__":
    pytest.main([__file__])
