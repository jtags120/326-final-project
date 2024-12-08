import passwordManager

def testAuth():
    '''Tests will test logins, i.e. password and username are correct inc. if
    password is empty'''
    pass

def testEncrypt():
    '''Tests will test encrypting and decrypting passwords, inc. empty passwords
    incorrect keys, or multiple encryption levels'''
    #single encryption
    encryptor = passwordManager.Encryptor()
    enc = encryptor.encrypt("password")
    assert encryptor.decrypt(enc) == "password"
    
    #double encryption
    encryptor2 = passwordManager.Encryptor()
    doubleEnc = encryptor2.encrypt(enc)
    print(encryptor.decrypt((encryptor2.decrypt(doubleEnc))))
    
    #empty password
    emptyEnc = encryptor.encrypt("")
    assert encryptor.decrypt(emptyEnc) == ""
    
    #incorrect key
    encryptor3 = passwordManager.Encryptor()
    incorrectEnc = encryptor3.encrypt("password")
    assert encryptor.decrypt(incorrectEnc) != "password"
    
    
    

def testDB():
    '''Tests will test database creation, insertion, and deletion
    Edge case would be empty database'''
    pass

def testUI():
    '''Tests will test the user interface, i.e. command line'''
    pass

def testEdge():
    '''Tests will test edge cases, i.e. empty password, long password(1000+ chars)
    empty passwords etc.'''
    pass

