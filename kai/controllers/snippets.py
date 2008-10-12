import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from couchdb import ResourceConflict
from kai.lib.base import BaseController, render
from kai.model import Snippet

log = logging.getLogger(__name__)

class SnippetsController(BaseController):

    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Snippets'

    def index(self):
        # Return a rendered template
        #   return render('/template.mako')
        # or, Return a response
        return render('snippets/index.mako')
        
    
    def add(self):
        
        return render('snippets/add.mako')