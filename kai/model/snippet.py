from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, DictField, Document, TextField, \
    ListField, FloatField, Schema, IntegerField, BooleanField

class Snippet(Document):
    type = TextField(default='Snippet')
    human_id = TextField()
    username = TextField()
    created = DateTimeField(default=datetime.now)
    title = TextField()
    description = TextField()
    content = TextField()
    slug = TextField()
    tags = ListField(TextField())
    all_ratings = DictField(Schema.build(
            human_id = TextField(),
            rating = IntegerField()
    ))
    computed_rating = FloatField()
    reported = BooleanField(default=False)
    reported_by = TextField() # human_id
    
    @classmethod
    def exists(cls, title):
        rows = pylons.c.db.view('snippets/by_title')[title]
        return len(rows) > 0
        
    @classmethod
    def by_date(cls, **options):
        options['include_docs'] = True
        return pylons.c.db.view('snippets/by_date', **options)
        
    @classmethod
    def by_author(cls, **options):
        return pylons.c.db.view('snippets/by_author', **options)
        
    @classmethod
    def by_author_id(cls, human_id, **options):
        options['include_docs'] = True
        return pylons.c.db.view('snippets/by_author_id', **options)[human_id]
        
    @classmethod
    def fetch_snippet(cls, slug, **options):
        options['include_docs'] = True
        snip = pylons.c.db.view('snippets/by_slug', **options)[slug]
        if snip.total_rows > 0:
            return snip.rows[0].doc
        else:
            return False
