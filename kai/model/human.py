import os
import sha
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, ListField


class Human(Document):
    """Represents a human user"""
    type = TextField(default='Human')
    displayname = TextField()
    email = TextField()
    password = TextField()
    created = DateTimeField(default=datetime.now)
    last_login = DateTimeField(default=datetime.now)
    blog = TextField()
    openid = ListField(TextField())
    session_id = TextField()
    
    @classmethod
    def get_displayname(cls, displayname, **options):
        options['include_docs'] = True
        rows = pylons.c.db.view('human/by_displayname', **options)[displayname]
        if len(rows) > 0:
            return cls.wrap(list(rows)[0].doc)
        else:
            return False
    
    @classmethod
    def get_email(cls, email, **options):
        options['include_docs'] = True
        rows = pylons.c.db.view('human/by_email', **options)[email]
        if len(rows) > 0:
            return cls.wrap(list(rows)[0].doc)
        else:
            return False
    
    @staticmethod
    def hash_password(plain_text):
        """Returns a crypted/salted password field
        
        The salt is stored in front of the password, for per user 
        salts.
        
        """
        if isinstance(plain_text, unicode):
            plain_text = plain_text.encode('utf-8')
        password_salt = sha.new(os.urandom(60)).hexdigest()
        crypt = sha.new(plain_text + password_salt).hexdigest()
        return password_salt + crypt
    
    def verify_password(self, plain_text):
        """Verify a plain text string is the users password"""  
        if isinstance(plain_text, unicode):
            plain_text = plain_text.encode('utf-8')
        password_salt = self.password[:40]
        crypt_pass = sha.new(plain_text + password_salt).hexdigest()
        if crypt_pass == self.password[40:]:
            return True
        else:
            return False
