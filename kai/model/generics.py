"""Generic functionality that applies to any CouchDB Document

This module handles generic functionality that works against any kind
of CouchDB document.

"""
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, FloatField, View

class Comment(Document):
    type = TextField(default='Comment')
    human_id = TextField()
    displayname = TextField()
    email = TextField()
    doc_id = TextField()
    content = TextField(default='')
    markup = TextField(default='textile')
    created = DateTimeField(default=datetime.utcnow)
    
    by_time = View('comments', '''
        function(doc) {
          if (doc.type == 'Comment') {
            emit([doc.doc_id, doc.created], null);
          }
        }''', include_docs=True)
    
    comment_count = View('comments', '''
        function(doc) {
          if (doc.type == 'Comment') {
            emit(doc.doc_id, 1);
          }
        }''', '''
        function(keys, values) {
          return sum(values);
        }''',
        wrapper= lambda row: (row.key, row.value), group=True)
    
    @classmethod
    def total_comments(cls, doc_id):
        comments = list(Comment.comment_count(pylons.c.db)[doc_id])
        if not comments:
            return 0
        else:
            return comments[0][1]


class Rating(Document):
    type = TextField(default='Rating')
    human_id = TextField()
    doc_id = TextField()
    displayname = TextField()
    rating = FloatField()
    time = DateTimeField(default=datetime.now)
    
    all_raters = View('rating', '''
        function(doc) {
          if (doc.type == 'Rating') {
            emit(doc.doc_id, {displayname:doc.displayname, id:doc._id});
          }
        }''', '''
        function(keys, values) {
          return values;
        }''',
        wrapper=lambda row: row.key,
        name='raters', group=True)
    
    @classmethod
    def has_rated(cls, doc_id, displayname, **options):
        """Checks the document to see if the displayname has already rated
        the document, if so, returns the id of the rating doc"""
        docs = list(cls.all_raters(pylons.c.db)[doc_id])
        if docs:
            for rating in docs[0]:
                if displayname == rating['displayname']:
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
