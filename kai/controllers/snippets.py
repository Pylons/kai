import logging
import re

from couchdb import ResourceConflict
from docutils.core import publish_parts
from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest
from tw.mods.pylonshf import validate

import kai.lib.pygmentsupport
from kai.lib.base import BaseController, render
from kai.lib.helpers import success_flash, failure_flash
from kai.model import Snippet, forms
from kai.model.generics import all_doc_tags

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
    
    @rest.dispatch_on(POST='_process_add')
    def add(self):
        if not c.user:
            abort(401)        
        c.tags = [row['name'] for row in list(all_doc_tags(self.db))]
        return render('snippets/add.mako')
    
    @validate(form=forms.snippet_form, error_handler='add')
    def _process_add(self):  
        if not c.user:
            abort(401)      
        snippet = Snippet(**self.form_result)
        snippet.human_id = c.user.id
        snippet.email = c.user.email
        snippet.displayname = c.user.displayname
        
        ## generate the slug
        slug = snippet.title.replace(" ", "_")
        slug = slug.lower()
        slug = re.sub('[^A-Za-z0-9_]+', '', slug)
        
        snippet.slug = slug
        if 'tags' in self.form_result:
            snippet.tags = self.form_result['tags'].replace(',', ' ').strip().split(' ')
        
        snippet.store(self.db)
        success_flash('Snippet has been added')
        return redirect_to('snippet_home')
    
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
