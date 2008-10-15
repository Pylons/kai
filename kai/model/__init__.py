"""CouchDB Models"""
import os
import sha
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, DictField, Document, TextField, \
    ListField, FloatField, Schema, IntegerField, BooleanField


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
        rows = pylons.c.db.view('human/by_displayname')[displayname]
        if len(rows) > 0:
            return cls.wrap(list(rows)[0].value)
        else:
            return False
    
    @classmethod
    def get_email(cls, email, **options):
        rows = pylons.c.db.view('human/by_email')[email]
        if len(rows) > 0:
            return cls.wrap(list(rows)[0].value)
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


class Paste(Document):
    type = TextField(default='Paste')
    human_id = TextField()
    username = TextField()
    created = DateTimeField(default=datetime.now)
    title = TextField()
    language = TextField()
    code = TextField()


class Snippet(Document):
    type = TextField(default='Snippet')
    human_id = TextField()
    username = TextField()
    created = DateTimeField(default=datetime.now)
    title = TextField()
    description = TextField()
    content = TextField()
    slug = TextField()
    tags = ListField(TextField())
    all_ratings = DictField(Schema.build(
            human_id = TextField(),
            rating = IntegerField()
    ))
    computed_rating = FloatField()
    reported = BooleanField(default=False)
    reported_by = TextField() # human_id
    
    @classmethod
    def exists(cls, title):
        rows = pylons.c.db.view('snippets/by_title')[title]
        return len(rows) > 0
        
    @classmethod
    def by_date(cls, **options):
        rows = pylons.c.db.view('snippets/by_date', **options)
        return rows
        
    @classmethod
    def by_author(cls, **options):
        rows = pylons.c.db.view('snippets/by_author', **options)
        return rows
        
    @classmethod
    def by_author_id(cls, human_id, **options):
        rows = pylons.c.db.view('snippets/by_author_id', **options)[human_id]
        return rows
        
    @classmethod
    def fetch_snippet(cls, slug, **options):
        snip = pylons.c.db.view('snippets/by_slug', **options)[slug]
        if snip.total_rows > 0:
            return snip.rows[0].value
        else:
            return False



class Comment(Document):
    type = TextField(default='Comment')
    human_id = TextField()
    doc_id = TextField()
    username = TextField()
    content = TextField(default='')
    markup = TextField(default='')
    time = DateTimeField()


class Documentation(object):
    @classmethod
    def fetch_doc(cls, project, version, path):
        rows = pylons.c.db.view('documentation/by_path')[[project, version, path]]
        if len(rows) > 0:
            return list(rows)[0].value
        else:
            return False
    
    @classmethod
    def delete_revision(cls, project, rev):
        rows = pylons.c.db.view('documentation/ids_for_version')[[project, rev]]
        for row in rows:
            del db[row.id]
    
    @classmethod
    def exists(cls, doc):
        key = [doc['filename'], doc['version'], doc['project']]
        rows = pylons.c.db.view('documentation/doc_key', group=True)[key]
        return len(rows) > 0
