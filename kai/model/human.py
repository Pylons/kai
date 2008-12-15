import os
import md5
import sha
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, ListField, View


class Human(Document):
    """Represents a human user"""
    type = TextField(default='Human')
    displayname = TextField()
    email = TextField()
    timezone = TextField()
    password = TextField()
    created = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(default=datetime.utcnow)
    blog = TextField()
    session_id = TextField()
    
    email_token = TextField()
    password_token = TextField()
    
    email_token_issue = DateTimeField()
    password_token_issue = DateTimeField()    
    
    openids = ListField(TextField())
    groups = ListField(TextField())
    
    by_openid = View('human', '''
        function(doc) {
          if (doc.type == 'Human' && doc.openids) {
            for (var idx in doc.openids) {
              emit(doc.openids[idx], null);
            }
          }
        }''', include_docs=True)
    
    by_displayname = View('human', '''
        function(doc) {
          if (doc.type == 'Human') {
            emit(doc.displayname, null);
          }
        }''', include_docs=True)
    
    by_email = View('human', '''
        function(doc) {
          if (doc.type == 'Human') {
            emit(doc.email, null);
          }
        }''', include_docs=True)
    
    by_email_token = View('human', '''
        function(doc) {
          if (doc.type == 'Human' && doc.email_token) {
            emit(doc.email_token, null);
          }
        }''', include_docs=True)
    
    by_password_token = View('human', '''
        function(doc) {
          if (doc.type == 'Human' && doc.password_token) {
            emit(doc.password_token, null);
          }
        }''', include_docs=True)
    
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
    
    def email_hash(self):
        return md5.md5(self.email).hexdigest()
    
    def generate_token(self):
        """Generate's a token for use either for forgot password or
        email verification"""
        return sha.new(os.urandom(60)).hexdigest()
    
    def valid_password_token(self):
        diff = datetime.now() - self.password_token_issue
        token_lifespan = pylons.config['sso.password_token_lifespan']
        if diff.days < 1 and diff.seconds < token_lifespan:
            return True
        else:
            return False
    
    def in_group(self, group):
        if group in list(self.groups):
            return True
        else:
            return False
    
    def process_login(self):
        session = pylons.session._current_obj()
        session['logged_in'] = True
        session['displayname'] = self.displayname
        session['user_id'] = self.id
        session.save()
        self.session_id = session.id
        self.store(pylons.c.db)
