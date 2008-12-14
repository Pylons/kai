import os
import sha
from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, ListField


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
            self.published = datetime.now()
        if update_timestamp or not self.updated:
            self.updated = datetime.now()
        Document.store(self, db)

    @classmethod
    def by_time(cls, **options):
        return cls.view(pylons.c.db, 'articles/by_time', **options)
