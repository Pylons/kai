"""To be run from inside the pylonshq project, with kai also installed"""
import pylons
from couchdb import Server, Database
from pytz import UTC

from kai.model import Human, Paste
from kai.model.generics import all_doc_tags

pylons.c.db = db = Database('http://localhost:25984/kai')


def make_couch_paste(old):
    from datetime import datetime
    from couchdb import Server, Database
    from pytz import UTC
    import pylons
    from kai.model import Human, Paste
    from kai.model.generics import all_doc_tags
    
    pylons.c.db = db = Database('http://localhost:25984/kai')
    
    od = old.date.astimezone(UTC)
    created = datetime(od.year, od.month, od.day, od.hour, od.minute, od.second)
    new = Paste(old_id=old.id, old_poster=old.author, title=old.title,
                code=old.code, language=old.language, created=created)
    for tag in old.tags:
        new.tags.append(tag.name)
    new.store(db)

results = model.Session.query(model.Paste).order_by(model.Paste.id.desc())
for result in results:
    doc = list(Paste.by_old_id(db)[str(result.id)])
    if doc:
        break
    make_couch_paste(result)