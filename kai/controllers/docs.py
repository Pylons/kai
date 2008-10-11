import logging

from couchdb import ResourceConflict
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from kai.lib.base import BaseController, json, render
from kai.model import Documentation

log = logging.getLogger(__name__)

class DocsController(BaseController):
    """Documentation Controller
    
    The Documentation controller handles uploads of docs, as well as
    doc display.
    
    """
    def __before__(self):
        c.active_tab = 'Documentation'
        c.active_sub = 'Reference'
    
    def view(self, version, url):
        if url.startswith('glossary/'):
            c.active_sub = 'Glossary'
        if url.startswith('modules/'):
            c.active_sub = 'Modules'
        if url == 'modules/':
            url = 'modindex'
        if url == 'index/':
            url = 'genindex'
            c.active_sub = 'Index'
        if url.endswith('/'):
            url = url[:-1]
        c.doc = Documentation.fetch_doc('Pylons', version, url)
        if not c.doc:
            # Try again with index just in case
            url += '/index'
            c.doc = Documentation.fetch_doc('Pylons', version, url)
            if not c.doc:
                abort(404)
        if url == 'modindex':
            return render('/docs/modindex.mako')
        if url == 'genindex':
            return render('/docs/genindex.mako')
        return render('/docs/view.mako')
    
    @jsonify
    def upload(self):
        try:
            doc = json.loads(request.body)
        except:
            response.status = 500
            return dict(status='error', reason='Unable to parse JSON')
        doc['type'] = 'Documentation'
        
        # Check to see we don't have it already
        if Documentation.exists(doc):
            response.status = 409
            return dict(status='conflict')
        
        try:
            self.db.create(doc)
        except ResourceConflict:
            response.status = 409
            return dict(status='conflict')
        return dict(status='ok')
