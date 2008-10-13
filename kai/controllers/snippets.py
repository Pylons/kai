import logging, datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from couchdb import ResourceConflict
from kai.lib.base import BaseController, render
from formencode import htmlfill
from kai.model import Snippet
from kai.model import forms
log = logging.getLogger(__name__)

class SnippetsController(BaseController):

    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Snippets'

    def index(self):
        snippets      = Snippet.by_date(descending=True, count=20)
        c.snippets      = [Snippet.wrap(row.value) for row in snippets]
        return render('snippets/index.mako')
        
        
    @validate(forms.AddSnippet(), form='add')
    def add(self):
        
        """ Simply add a code snippet to the database. """
        
        c.exists    = False
        c.add_error = None
        added       = False
        
        if hasattr(self, 'form_result'):
            snippet                 = Snippet()
            snippet.title           = self.form_result.get('title')
            snippet.description     = self.form_result.get('description')
            snippet.content         = self.form_result.get('content')
            snippet.type            = 'Snippet'
            snippet.human_id        = 1
            snippet.created         = datetime.datetime.now()
            snippet.username        = 'Andy-Test - Username'
            
            if Snippet.exists(snippet.title):
                c.exists        = True
                return htmlfill.render(render('snippets/add.mako'), self.form_result)
            else:
                try:
                    snippet.store(self.db)
                    added       = True
                except Exception, e:
                    c.add_error = True
                    c.error     = e
            
            if added:
                return redirect_to('snippet_home')
        
        return render('snippets/add.mako')
        
    def view(self, id):
        c.snippet     = Snippet.fetch_snippet(id)
        print c.snippet
        return "testing"