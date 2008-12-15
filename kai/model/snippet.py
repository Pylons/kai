from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, DictField, Document, TextField, \
    ListField, FloatField, Schema, IntegerField, BooleanField, View

class Snippet(Document):
    type = TextField(default='Snippet')
    human_id = TextField()
    displayname = TextField()
    created = DateTimeField(default=datetime.utcnow)
    title = TextField()
    description = TextField()
    content = TextField()
    slug = TextField()
    tags = ListField(TextField())
    reported = BooleanField(default=False)
    reported_by = TextField() # human_id
    
    all_tags = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet' && doc.tags) {
            for (var idx in doc.tags) {
              var tag = doc.tags[idx];
              tag = tag.replace(/ /g, '');
              if (tag) {
                emit(tag, 1);
              }
            }
          }
        }''', '''
        function(keys, values) {
          return sum(values);
        }''',
        wrapper=lambda row: row.key,
        name='tags', group=True)
    
    by_tag = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet' && doc.tags) {
            for (var idx in doc.tags) {
            var tag = doc.tags[idx];
            tag = tag.replace(/ /g, '');
            if (tag) {
              emit(tag, null);
            }
            }
          }
        }''', include_docs=True)
    
    by_title = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet' && doc.title) {
            emit(doc.title, 1);
          }
        }''')
    
    by_date = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet') {
            emit(doc.created, null);
          }
        }''', include_docs=True)
    
    by_author = View('snippets', '''
        function (doc) {
          if (doc.type == 'Snippet') {
            emit(doc.displayname, null);
          }
        }''', include_docs=True)
    
    author_totals = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet') {
            emit([doc.displayname, doc.human_id], 1);
          }
        }''', '''
        function (key, values) {
          return sum(values);
        }''',
        wrapper=lambda row: {'author':row.key[0],
                             'id':row.key[1],
                             'amount':row.value},
        group=True)
    
    by_author_id = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet' && doc.human_id) {
            emit(doc.human_id, null);
          }
        }''', include_docs=True)
    
    by_slug = View('snippets', '''
        function(doc) {
          if (doc.type == 'Snippet' && doc.slug) {
            emit(doc.slug, null);
          }
        }''', include_docs=True)
    
    @classmethod
    def exists(cls, title):
        rows = pylons.c.db.view('snippets/by_title')[title]
        return len(rows) > 0
