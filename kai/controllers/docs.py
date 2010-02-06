import mimetypes
import logging
import os

from couchdb import ResourceConflict
from paste.urlparser import StaticURLParser
from pylons import config, request, response, session, tmpl_context as c
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
    
    def view(self, version, url, language):
        # Change the url back to a string (just in case)
        url = str(url)
        
        if 'doc_version' not in session or version != session['doc_version']:
            session['doc_version'] = version
            session.save()
        
        # Check for serving images
        if url.startswith('_images/'):
            img_srv = StaticURLParser(config['image_dir'])
            request.environ['PATH_INFO'] = '/Pylons/%s/%s' % (version, url[8:])
            return img_srv(request.environ, self.start_response)
        
        # If the docs are pre-0.9.7, use the old viewer
        if version < '0.9.7':
            return self._view_old(version, url)
        
        # Check a few other space cases and alter the URL as needed
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
        
        # Grab the doc from CouchDB
        c.doc = Documentation.fetch_doc('Pylons', version, language, url)
        if not c.doc:
            # Try again with index just in case
            url += '/index'
            c.doc = Documentation.fetch_doc('Pylons', version, language, url)
            if not c.doc:
                abort(404)
        if url == 'modindex':
            return render('/docs/modindex.mako')
        if url == 'genindex':
            return render('/docs/genindex.mako')
        if url == 'objects.inv':
            response.content_type = 'text/plain'
            return c.doc['content']
        
        if url == 'search':
            redirect_to('search')
        return render('/docs/view.mako')
    
    def _view_old(self, version, url):
        if request.path_info.endswith('docs') or request.path_info.endswith('docs/'):
            redirect_to('/docs/%s/' % str(version))

        base_path = os.path.normpath(config.get('doc_dir'))
        if url == 'index':
            url = 'index.html'
        c.url = os.path.normpath(os.path.join(base_path, version, url))
        
        # Prevent circumvention of the base docs path and bad paths
        if not c.url.startswith(base_path) or not os.path.exists(c.url):
            if version > '0.9.5':
                redirect_to('cdocs', page='Home')
            abort(404)
        c.version = version
        return render('/docs/load_content.mako')
        
    @jsonify
    def upload_image(self):
        dockey = config['doc.security_key']
        if request.environ['HTTP_AUTHKEY'] != dockey:
            abort(401)
        doc = request.body
        
        version = request.GET.get('version')
        project = request.GET.get('project')
        name = request.GET.get('name')
        if not version or not project or not name:
            response.status = 500
            return dict(status='error', reason='No version/project combo found')
        fdir = os.path.join(config['image_dir'], project, version)
        
        # Ensure this didn't escape our current dir, we must be under images
        if not fdir.startswith(config['image_dir']):
            abort(500)
        
        fname = os.path.join(fdir, name)
        
        # Ensure we're under the parent dir we should be
        if not fname.startswith(fdir):
            abort(500)
        ensure_dir(fdir)
        try:
            with open(os.path.join(fdir, name), 'w') as w:
                w.write(doc)
        except:
            abort(500)
        else:
            return dict(status='ok')
    
    @jsonify
    def upload(self):
        dockey = config['doc.security_key']
        if request.environ['HTTP_AUTHKEY'] != dockey:
            abort(401)
        
        try:
            doc = json.loads(request.body)
        except:
            response.status = 500
            return dict(status='error', reason='Unable to parse JSON')
        doc['type'] = 'Documentation'
        
        update = False
        # Check to see we don't have it already
        existing_doc = list(Documentation.doc_key(self.db)[doc['filename'], doc['version'], doc['language'], doc['project']])
        if existing_doc:
            existing_doc = dict(existing_doc[0].doc)
            update = True
        try:
            if update:
                existing_doc.update(doc)
                self.db.update([existing_doc])
            else:
                self.db.create(doc)
        except ResourceConflict:
            response.status = 409
            return dict(status='conflict')
        return dict(status='ok')
    
    @jsonify
    def delete_revision(self, project, version):
        dockey = config['doc.security_key']
        if request.environ['HTTP_AUTHKEY'] != dockey:
            abort(401)
        
        # Documentation.delete_revision(project, version)
        return dict(status='ok')


def ensure_dir(dir):
    """Copied from Mako, ensures a directory exists in the filesystem"""
    tries = 0
    while not os.path.exists(dir):
        try:
            tries += 1
            os.makedirs(dir, 0750)
        except:
            if tries > 5:
                raise
