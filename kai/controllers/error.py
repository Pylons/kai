import cgi
import os.path

from paste.urlparser import StaticURLParser
from pylons import tmpl_context as c, request
from pylons.controllers.util import abort, forward
from pylons.middleware import error_document_template, media_path
from webhelpers.html.builder import literal

from kai.lib.base import BaseController, render

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.
    
    """
    def document(self):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        if not resp:
            abort(404)
        c.prefix = request.environ.get('SCRIPT_NAME', '')
        c.code = str(request.params.get('code', resp.status_int))
        c.message = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
        return render('error.mako')

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file(os.path.join(media_path, 'img'), id)

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file(os.path.join(media_path, 'style'), id)

    def _serve_file(self, root, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        static = StaticURLParser(root)
        request.environ['PATH_INFO'] = '/%s' % path
        return static(request.environ, self.start_response)
