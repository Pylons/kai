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
        """ Get the snippets by date and by author"""
        snippets = list(Snippet.by_date(self.db, descending=True, count=100))
        c.snippets = snippets[:20]
        authors = []
        for snippet in c.snippets:
            displayname = snippet.displayname.strip()
            if displayname not in authors:
                authors.append(displayname)        
        c.unique_authors = authors[:10]
        return render('/snippets/index.mako')
    
    @validate(forms.AddSnippet(), form='add')
    def add(self):
        """ Simply add a code snippet to the database. """
        if not c.user:
            abort(401)
        
        c.exists = False
        c.add_error = None
        added = False
        
        if hasattr(self, 'form_result'):
            snippet = Snippet(**self.form_result)
            snippet.human_id = c.user.id
            snippet.displayname = c.user.displayname
            
            ## generate the slug
            slug = snippet.title.replace(" ", "_")
            slug = slug.lower()
            slug = re.sub('[^A-Za-z0-9_]+', '', slug)
            
            snippet.slug = slug
            snippet.tags = self.form_result.get('tags').lower().split(",")           
            
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
        """View a particular snippet
        
        Keyword arguments:
        id - actually a slug
        
        """
        slug = id.lower().strip()
        snippets = list(Snippet.by_slug(self.db)[slug]) or abort(404)
        snippet = snippets[0]
        
        defaults = {
            'file_insertion_enabled': 0,
            'raw_enabled': 0,
            'input_encoding': 'unicode',
        }
        string = publish_parts(snippet.content, writer_name='html',
                               settings_overrides=defaults)['html_body']
            
        c.snippet_content = string
        c.snippet = snippet
        return render('/snippets/view.mako')
    
    def by_author(self, id=None):
        """View snippets by an authors human_id.
        
        Keyword arguments:
        id - authors human id.
        
        """
        if not id:
            c.authors = list(Snippet.author_totals(self.db))
        else:
            snippets = list(Snippet.by_author(self.db)[id]) or abort(404)
            c.username = snippets[0].displayname
            c.snippets = snippets
        return render('/snippets/byauthor.mako')
        
    def by_tag(self, tag=None):
        """View snippets by a particular tag.
        
        Keyword arguments:
        tag - a tag (string)
        
        """
        snippets = list(Snippet.by_tag(self.db)[tag]) or abort(404)
        c.snippets = snippets
        c.tag = tag
        return render('/snippets/bytag.mako')
    
    def tagcloud(self):
        c.tag_sizes = Snippet.tag_sizes()
        return render('/snippets/tagcloud.mako')
