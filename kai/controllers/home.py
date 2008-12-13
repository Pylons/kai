import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):
    def index(self):
        return render('/home/index.mako')
    
    def history(self):
        c.active_sub = 'History'
        return render('/home/history.mako')
