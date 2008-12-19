from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, ListField, TextField, View


class Paste(Document):
    type = TextField(default='Paste')
    human_id = TextField()
    displayname = TextField()
    email = TextField()
    created = DateTimeField(default=datetime.utcnow)
    title = TextField()
    language = TextField()
    code = TextField()
    
    tags = ListField(TextField())

    old_id = TextField()
    old_poster = TextField()
    
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

    @classmethod
    def tag_sizes(cls):
        """This method returns all the tags and their relative size for
        a tagcloud"""
        tags = list(cls.all_tags(pylons.c.db))
        totalcounts = []
        for tag in tags:
            weight = (math.log(tag['count'] or 1) * 4) + 10
            totalcounts.append((tag['name'], tag['count'], weight))
        return sorted(totalcounts, cmp=lambda x,y: cmp(x[0], y[0]))
