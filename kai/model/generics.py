"""Generic functionality that applies to any CouchDB Document

This module handles generic functionality that works against any kind
of CouchDB document.

"""
import pylons
from couchdb.schema import DateTimeField, Document, TextField, FloatField

class Comment(Document):
    type = TextField(default='Comment')
    human_id = TextField()
    doc_id = TextField()
    username = TextField()
    content = TextField(default='')
    markup = TextField(default='')
    time = DateTimeField()


class Rating(Document):
    type = TextField(default='Rating')
    human_id = TextField()
    doc_id = TextField()
    username = TextField()
    rating = FloatField()
    
    @classmethod
    def by_id(cls, doc_id, **options):
        """Retrieves the overall rating for a document"""
        rows = pylons.c.db.view('rating/by_id', **options)[doc_id]
        if len(rows) > 0:
            return list(rows)[0].value
        else:
            return None
    
    @classmethod
    def add_rating(cls, doc_id, user, rating):
        """Add's a rating to the database for a given user, to
        the given doc id with the provided rating
        
        user must be a user object with a id, and username in it
        
        """
        new_rating = cls(human_id=user.id, doc_id=doc_id,
                         username=user.displayname, rating=rating)
        new_rating.store(pylons.c.db)
