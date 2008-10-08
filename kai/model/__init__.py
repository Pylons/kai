"""CouchDB Models"""
from datetime import datetime

from couchdb.schema import DateTimeField, DictField, Document, TextField, \
    ListField


class Human(Document):
    """Represents a human user"""
    type = TextField(default='Human')
    name = TextField()
    username = TextField()
    created = DateTimeField(default=datetime.now)
    last_login = DateTimeField(default=datetime.now)
    blog = TextField()
    openid = ListField(TextField())


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


class Comment(Document):
    type = TextField(default='Comment')
    human_id = TextField()
    doc_id = TextField()
    username = TextField()
    content = TextField(default='')
    markup = TextField(default='')
    time = DateTimeField()
    
