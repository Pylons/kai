import logging
import re

from couchdb import ResourceConflict
from docutils.core import publish_parts
from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate

import kai.lib.pygmentsupport
from kai.lib.base import BaseController, render
from kai.model import Snippet, forms

log = logging.getLogger(__name__)

class SnippetsController(BaseController):
    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Snippets'

    def index(self):
        snippets = Snippet.by_date(descending=True, count=20)
        c.snippets = [Snippet.wrap(row.value) for row in snippets]
        return render('snippets/index.mako')
    
    @validate(forms.AddSnippet(), form='add')
    def add(self):
        """ Simply add a code snippet to the database. """
        
        c.exists = False
        c.add_error = None
        added = False
        
        if hasattr(self, 'form_result'):
            snippet = Snippet(**self.form_result)
            snippet.human_id = 1
            snippet.username = 'Andy-Test - Username'
            
            ## generate the slug
            slug = snippet.title.replace(" ", "_")
            slug = slug.lower()
            slug = re.sub('[^A-Za-z0-9_]+', '', slug)
            
            snippet.slug = slug
            snippet.tags = self.form_result.get('tags')            
            
            if Snippet.exists(snippet.title):
                c.exists = True
                return htmlfill.render(render('snippets/add.mako'), self.form_result)
            else:
                try:
                    snippet.store(self.db)
                    added = True
                except Exception, e:
                    c.add_error = True
                    c.error = e
            
            if added:
                return redirect_to('snippet_home')
        
        return render('snippets/add.mako')
    
    def view(self, id):
        slug = id.lower().strip()
        snippet = Snippet.wrap(Snippet.fetch_snippet(slug))
        
        defaults = {
            'file_insertion_enabled': 0,
            'raw_enabled': 0,
            'input_encoding': 'unicode',
        }
        string = publish_parts(snippet.content, writer_name='html',
                               settings_overrides=defaults)['html_body']
            
        c.snippet_content = string
        c.snippet = snippet
        return render('snippets/view.mako')