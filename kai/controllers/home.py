import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.model import Article

log = logging.getLogger(__name__)

class HomeController(BaseController):
    def index(self):
        c.news = list(Article.by_time(descending=True, count=5))
        return render('/home/index.mako')
    
    def history(self):
        c.active_sub = 'History'
        return render('/home/history.mako')
