from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, Document, TextField, View


class Paste(Document):
    type = TextField(default='Paste')
    human_id = TextField()
    displayname = TextField()
    created = DateTimeField(default=datetime.utcnow)
    title = TextField()
    language = TextField()
    code = TextField()

