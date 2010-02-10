import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from kai.lib.base import BaseController, render
from kai.model import Article, Comment, Snippet, Paste
from kai.websetup import sync_db

log = logging.getLogger(__name__)

class HomeController(BaseController):
    def sync(self):
        if not request.environ['toppcloud.internal']:
            abort(404)
        sync_db(c.db)

    def index(self):
        c.articles = list(Article.by_time(c.db, descending=True, limit=5))
        c.snippets = list(Snippet.by_date(c.db, descending=True, limit=7))
        c.pastes = list(Paste.by_time(c.db, descending=True, limit=5))
        return render('/home/index.mako')
    
    def robots(self):
        response.content_type = 'text/plain'
        return render('/home/robots.mako')
        
    def history(self):
        c.active_sub = 'History'
        return render('/home/history.mako')

    def features(self):
        c.active_sub = 'Features'
        return render('/home/features.mako')
    
    def search(self):
        c.active_sub = 'Search'
        return render('/search.mako')
    
    def community(self):
        c.active_tab = 'Community'
        c.active_sub = True
        
        # Load various latest data
        c.snippets = list(Snippet.by_date(c.db, descending=True, limit=5))
        c.pastes = list(Paste.by_time(c.db, descending=True, limit=10))
        
        # Pull comments and grab the docs with them for their info
        comments = list(Comment.by_anytime(c.db, descending=True, limit=10))
        commentdata = []
        for comment_doc in comments:
            comment = {}
            comment['displayname'] = comment_doc.displayname or 'Anonymous'
            comment['created'] = comment_doc.created
            comment['email'] = comment_doc.email or 'anonymous'
            comment['content'] = comment_doc.content
            comment['id'] = comment_doc.id
            doc = c.db.get(comment_doc.doc_id)
            if doc['type'] == 'Traceback':
                comment['title'] = '%s: %s' % (doc['exception_type'], doc['exception_value'])
            else:
                comment['title'] = doc.get('title', '-- No title --')
            comment['type'] = doc['type']
            comment['doc'] = doc
            comment['doc_id'] = comment_doc.doc_id
            commentdata.append(comment)
        c.comments = commentdata
        return render('/home/community.mako')