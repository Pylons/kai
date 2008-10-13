"""CouchDB Models"""
import pylons
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
    
    @classmethod
    def exists(cls, title):
        rows    = pylons.c.db.view('snippets/by_title')[title]
        return len(rows) > 0
        
    @classmethod
    def by_date(cls, **options):
        rows    = pylons.c.db.view('snippets/by_date', **options)
        return rows
        
    @classmethod
    def by_author(cls):
        pass
        
    @classmethod
    def fetch_snippet(cls, title):
        pass


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
