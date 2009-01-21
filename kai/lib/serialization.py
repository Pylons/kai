import datetime

from couchdb.schema import Document
from webhelpers.feedgenerator import Atom1Feed

def render_feed(title, link, description, objects, pub_date=None):
    feed = Atom1Feed(title=title, link=link, description=description)
    for obj in objects:
        if isinstance(obj, dict):
            title = obj.get('title', 'No title')
            link = obj.get('link', '')
            description = obj.get('description', '')
            if pub_date:
                date = obj.get(pub_date)
            else:
                date = obj.get('feed_pub_date', '')
        else:
            title = obj.feed_title
            link = obj.feed_link
            description = obj.feed_description
            if pub_date:
                date = getattr(obj, pub_date)
            else:
                date = obj.feed_pub_date
        feed.add_item(title=title, link=link, pubdate=date, description=description)
    return feed.writeString('utf-8')
