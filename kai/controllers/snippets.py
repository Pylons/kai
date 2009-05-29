import logging
import re

from couchdb import ResourceConflict
from formencode import htmlfill
from pylons import cache, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest
from tw.mods.pylonshf import validate

import kai.lib.pygmentsupport
from kai.lib.base import BaseController, CMSObject, render
from kai.lib.decorators import logged_in
from kai.lib.helpers import success_flash, failure_flash, rst_render
from kai.lib.serialization import render_feed
from kai.model import Human, Snippet, forms
from kai.model.generics import all_doc_tags

log = logging.getLogger(__name__)

class SnippetsController(BaseController, CMSObject):    
    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Snippets'
    
    def preview(self):
        data = request.POST['content']
        return rst_render(data)

    def index(self, format='html'):
        """ Get the snippets by date and by author"""
        snippets = list(Snippet.by_date(self.db, descending=True, limit=100))
        c.snippets = snippets[:20]
        if format in ['atom', 'rss']:
            response.content_type = 'application/atom+xml'
            return render_feed(
                title="PylonsHQ Snippet Feed", link=url(qualified=True), 
                description="Recent PylonsHQ snippets", objects=c.snippets,
                pub_date='created')

        authors = []
        for snippet in c.snippets:
            displayname = snippet.displayname.strip()
            if displayname not in authors:
                authors.append(displayname)        
        c.unique_authors = authors[:10]
        return render('/snippets/index.mako')
    
    def new(self):
        if not c.user:
            abort(401)        
        c.tags = [row['name'] for row in list(all_doc_tags(self.db))]
        return render('snippets/add.mako')
    
    @validate(form=forms.snippet_form, error_handler='new')
    def create(self):
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
        redirect_to('snippets')

    @logged_in
    def edit(self, id):
        slug = id.lower().strip()
        snippets = list(Snippet.by_slug(self.db)[slug]) or abort(404)
        snippet = snippets[0]
        if snippet.displayname:
            author = Human.load(self.db, snippet.human_id)
        is_owner = self._check_owner(snippet, c.user, check_session=True)
        if not is_owner:
            abort(401)
        
        c.snippet = snippet
        return render('/snippets/edit.mako')
    
    @logged_in
    @validate(form=forms.snippet_form, error_handler='edit')
    def update(self, id):
        slug = id.lower().strip()
        snippets = list(Snippet.by_slug(self.db)[slug]) or abort(404)
        snippet = snippets[0]
        if snippet.displayname:
            author = Human.load(self.db, snippet.human_id)
        is_owner = self._check_owner(snippet, c.user, check_session=True)
        if not is_owner:
            abort(401)
        
        snippet.title = self.form_result['title']
        snippet.content = self.form_result['content']
        snippet.description = self.form_result['description']
        
        ## generate the slug
        slug = snippet.title.replace(" ", "_")
        slug = slug.lower()
        slug = re.sub('[^A-Za-z0-9_]+', '', slug)
        
        snippet.slug = slug
        if 'tags' in self.form_result:
            snippet.tags = self.form_result['tags'].replace(',', ' ').strip().split(' ')
        snippet.store(self.db)
        success_flash('Snippet has been updated')
        redirect_to('snippet', id=slug)
    
    @logged_in
    def preview(self):
        """Return a HTML version of the rST content"""
        data = request.POST['content']
        return rst_render(data)
    
    def show(self, id):
        """Show a particular snippet
        
        Keyword arguments:
        id - actually a slug
        
        """
        slug = id.lower().strip()
        snippets = list(Snippet.by_slug(self.db)[slug]) or abort(404)
        snippet = snippets[0]        
        c.snippet_content = rst_render(snippet.content)
        c.snippet = snippet
        if c.snippet.displayname:
            c.author = Human.load(self.db, c.snippet.human_id)
        c.is_owner = self._check_owner(c.snippet, c.user, check_session=True)
        
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
        c.tag_sizes = cache.get_cache('snippets.py_tagcloud').get_value(
            'snippet', createfunc=lambda: Snippet.tag_sizes(), expiretime=180)
        return render('/snippets/tagcloud.mako')
