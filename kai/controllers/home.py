import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.model import Article, Snippet, Paste

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
