import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from kai.lib.base import BaseController, render
from kai.model import Article

log = logging.getLogger(__name__)

class ArticlesController(BaseController):
    def __before__(self):
        c.active_tab = 'Community'
        c.active_sub = 'Blog'
    
    def index(self):
        c.articles = list(Article.by_time(descending=True, count=10))
        return render('/articles/index.mako')
