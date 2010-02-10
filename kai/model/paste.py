import math
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, ListField, TextField, View

from kai.lib.highlight import code_highlight, langdict


class Paste(Document):
    type = TextField(default='Paste')
    human_id = TextField()
    displayname = TextField()
    email = TextField()
    session_id = TextField()
    created = DateTimeField(default=datetime.utcnow)
    title = TextField()
    language = TextField()
    code = TextField()
    
    tags = ListField(TextField())

    old_id = TextField()
    old_poster = TextField()
    
    @classmethod
    def load(cls, db, id):
        """Load the obj, fall back to old id if needed"""
        obj = super(Paste, cls).load(db, id)
        if not obj:
            obj = cls.by_old_id(db)[id]
            if obj:
                return list(obj)[0]
        return obj
    
    @property
    def feed_title(self):
        return self.title
    
    @property
    def feed_link(self):
        return pylons.url('paste', id=self.old_id or self.id, qualified=True)
    
    @property
    def feed_description(self):
        content = "<p>Created by %s, Language: %s</p>" % \
            (self.displayname or 'Anonymous', langdict[self.language])
        content += code_highlight(self)
        return content
        
    all_tags = View('pastes', '''
        function(doc) {
          if (doc.type == 'Paste' && doc.tags) {
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
        wrapper=lambda row: {'name':row.key, 'count':row.value},
        name='tags', group=True)
    
    by_tag = View('pastes', '''
        function(doc) {
          if (doc.type == 'Paste' && doc.tags) {
            for (var idx in doc.tags) {
            var tag = doc.tags[idx];
            tag = tag.replace(/ /g, '');
            if (tag) {
              emit(tag, null);
            }
            }
          }
        }''', include_docs=True)

    by_author = View('pastes', '''
        function (doc) {
          if (doc.type == 'Paste' && doc.human_id) {
            emit(doc.human_id, null);
          }
        }''', include_docs=True)
    
    by_time = View('pastes', '''
        function (doc) {
          if (doc.type == 'Paste') {
            emit(doc.created, null);
          }
        }''', include_docs=True)
    
    by_tag_time = View('pastes', '''
        function (doc) {
          if (doc.type == 'Paste' && doc.tags) {
            for (var idx in doc.tags) {
              var tag = doc.tags[idx];
              tag = tag.replace(/ /g, '');
              if (tag) {
                emit([tag, doc.created], null);
              }
            }
          }
        }''', include_docs=True)
    
    by_session_id = View('pastes', '''
        function (doc) {
          if (doc.type == 'Paste' && doc.session_id) {
            emit(doc.session_id, null);
          }
        }''', include_docs=True)
    
    by_old_id = View('pastes', '''
        function (doc) {
          if (doc.type == 'Paste' && doc.old_id) {
            emit(doc.old_id, null);
          }
        }''', include_docs=True)
    
    @classmethod
    def tag_sizes(cls):
        """This method returns all the tags and their relative size for
        a tagcloud"""
        tags = list(cls.all_tags(pylons.tmpl_context.db))
        totalcounts = []
        for tag in tags:
            weight = (math.log(tag['count'] or 1) * 4) + 10
            totalcounts.append((tag['name'], tag['count'], weight))
        return sorted(totalcounts, cmp=lambda x,y: cmp(x[0], y[0]))

    @classmethod
    def associate_pasties(cls, user):
        db = pylons.tmpl_context.db
        pasties = list(cls.by_session_id(db)[pylons.session.id])
        if pasties:
            for paste in pasties:
                try:
                    paste.session_id = None
                    paste.human_id = user.id
                    paste.displayname = user.displayname
                    paste.email = user.email
                    paste.store(db)
                except:
                    pass
