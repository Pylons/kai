"""The base Controller API

Provides the BaseController class for subclassing.
"""
from couchdb import Database
from paste.deploy.converters import asbool
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
import simplejson as json
import pylons

from kai.model import Human

class BaseController(WSGIController):
    def _setup(self):
        """Do basic request setup"""
        if pylons.session.get('logged_in', False):
            user = Human.load(self.db, pylons.session.get('user_id'))
            if not user or user.session_id != pylons.session.id:
                user = 'Anonymous'
                pylons.session['logged_in'] = False
        else:
            user = 'Anonymous'
        pylons.c.user = user
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        pylons.c.db = self.db = Database(pylons.config['couchdb_uri'])
        self._setup()
        
        pylons.c.use_minified_assets = asbool(
            pylons.config.get('use_minified_assets', 'false'))
        return WSGIController.__call__(self, environ, start_response)

# Monkey patch httplib to buffer
import httplib
class HTTPResponse(httplib.HTTPResponse):
    def __init__(self, sock, **kw):
        httplib.HTTPResponse.__init__(self, sock, **kw)
        self.fp = sock.makefile('rb') 
httplib.HTTPConnection.response_class = HTTPResponse
