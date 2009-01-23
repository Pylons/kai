import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.model import Article, Comment, Snippet, Paste

log = logging.getLogger(__name__)

class HomeController(BaseController):
    def index(self):
        c.articles = list(Article.by_time(c.db, descending=True, count=5))
        c.snippets = list(Snippet.by_date(c.db, descending=True, count=7))
        c.pastes = list(Paste.by_time(c.db, descending=True, count=5))
        return render('/home/index.mako')
    
    def history(self):
        c.active_sub = 'History'
        return render('/home/history.mako')

    def features(self):
        c.active_sub = 'Features'
        return render('/home/features.mako')
    
    def search(self):
        return render('/search.mako')
    
    def community(self):
        c.active_tab = 'Community'
        c.active_sub = True
        
        # Load various latest data
        c.snippets = list(Snippet.by_date(c.db, descending=True, count=10))
        c.pastes = list(Paste.by_time(c.db, descending=True, count=10))
        
        # Pull comments and grab the docs with them for their info
        comments = list(Comment.by_time(c.db, descending=True, count=20))
        comment_docids = [comment.doc_id for comment in comments]
        comment_docs = c.db.get(comment_docids)
        
        return render('/home/community.mako')