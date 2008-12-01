"""Generic functionality that applies to any CouchDB Document

This module handles generic functionality that works against any kind
of CouchDB document.

"""
from datetime import datetime

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
    time = DateTimeField(default=datetime.now)
    
    @classmethod
    def has_rated(cls, doc_id, username, **options):
        """Checks the document to see if the username has already rated
        the document, if so, returns the id of the rating doc"""
        rows = pylons.c.db.view('rating/all_raters', **options)[doc_id]
        if len(rows) > 0:
            ratings = list(rows)[0].value
            for rating in ratings:
                if username == rating['username']:
                    return rating['id']
        return False
    
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
        
        If the user has already rated the document, this will update
        the rating to the new value
        
        """
        prior_rating = cls.has_rated(doc_id, user.displayname)
        if prior_rating:
            rating_doc = Rating.load(pylons.c.db, prior_rating)
        else:
            rating_doc = cls(human_id=user.id, doc_id=doc_id,
                         username=user.displayname)
        rating_doc.rating = rating
        rating_doc.store(pylons.c.db)
