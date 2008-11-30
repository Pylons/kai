from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField


class Paste(Document):
    type = TextField(default='Paste')
    human_id = TextField()
    username = TextField()
    created = DateTimeField(default=datetime.now)
    title = TextField()
    language = TextField()
    code = TextField()

