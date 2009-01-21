import os
import sha
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, ListField, View

from kai.lib.helpers import textilize

class Article(Document):
    """Represents an article"""
    type = TextField(default='Article')
    slug = TextField()
    title = TextField()
    human_id = TextField()
    author = TextField(default='anonymous')
    summary = TextField(default='')
    body = TextField(default='')
    extended = TextField(default='')
    published = DateTimeField()
    updated = DateTimeField()

    tags = ListField(TextField())

    @property
    def feed_title(self):
        return self.title
    
    @property
    def feed_link(self):
        return pylons.url('article_archives', article=self)
    
    @property
    def feed_description(self):
        return textilize(self.body)
    
    @property
    def atom_id(self):
        host = pylons.request.host
        if ':' in host:
            host = host.split(':', 1)[0]
        return 'tag:%s,%04d-%02d-%02d:%s' % (
            host, self.published.year, self.published.month,
            self.published.day, self.id
        )

    def store(self, db, update_timestamp=True):
        if not self.published:
            self.published = datetime.utcnow()
        if update_timestamp or not self.updated:
            self.updated = datetime.utcnow()
        Document.store(self, db)

    all_months = View('articles', '''
        function(doc) {
          if (doc.type == 'Article') {
            var year = parseInt(doc.published.substr(0, 4), 10);
            var month = parseInt(doc.published.substr(5, 2), 10);
            emit([year, month], 1);
          }
        }''', '''
        function(keys, values) {
          return sum(values);
        }''',
        wrapper=lambda row: datetime(row.key[0], row.key[1], 1),
        name='months', group=True)

    all_tags = View('articles', '''
        function(doc) {
          if (doc.type == 'Article' && doc.tags) {
            for (var idx in doc.tags) {
              emit(doc.tags[idx], 1);
            }
          }
        }''', '''
        function(keys, values) {
          return sum(values);
        }''',
        wrapper=lambda row: row.key,
        name='tags', group=True)
    
    by_month = View('articles', '''
        function(doc) {
          if (doc.type == 'Article') {
            var year = parseInt(doc.published.substr(0, 4), 10);
            var month = parseInt(doc.published.substr(5, 2), 10);
            emit([year, month, doc.published], {
              slug: doc.slug, title: doc.title, author: doc.author,
              summary: doc.summary, published: doc.published,
              updated: doc.updated, tags: doc.tags
            });
          }
        }''')

    by_tag = View('articles', u'''
        function(doc) {
          if (doc.type == 'Article' && doc.tags) {
            for (var idx in doc.tags) {
              emit([doc.tags[idx], doc.published], {
                slug: doc.slug, title: doc.title, author: doc.author,
                published: doc.published, updated: doc.updated,
                summary: doc.summary, body: doc.body, tags: doc.tags,
                extended: doc.extended != '' ? '...' : null
              });
            }
          }
        }''')

    by_time = View('articles', '''
        function(doc) {
          if (doc.type == 'Article') {
            emit(doc.published, 
                 {slug:doc.slug, title:doc.title, 
                  author:doc.author, body:doc.body,
                  published:doc.published, summary:doc.summary});
          }
        }''')
    
    by_slug = View('articles', '''
        function(doc) {
          if (doc.type == 'Article') {
            var year = parseInt(doc.published.substr(0, 4), 10);
            var month = parseInt(doc.published.substr(5, 2), 10);
            emit([year, month, doc.slug], null)
          }
        }''')
