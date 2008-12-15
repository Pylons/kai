"""The base Controller API

Provides the BaseController class for subclassing.
"""
from babel import Locale, UnknownLocaleError
from babel.support import Format
from babel.util import UTC
from couchdb import Database
from paste.deploy.converters import asbool
from pylons.controllers import WSGIController
from pylons.i18n import add_fallback, get_lang, set_lang
from pylons.templating import render_mako
from pytz import timezone
import simplejson as json
import pylons

from kai.model import Human

def render(template_name, **kwargs):
    """Render override that add's babel objects"""
    extra_vars = kwargs.pop('extra_vars', {})
    c = pylons.c._current_obj()
    extra_vars['format'] = c._format
    extra_vars['locale'] = c._locale
    extra_vars['timezone'] = c._tzinfo
    return render_mako(template_name, extra_vars=extra_vars, **kwargs)


class BaseController(WSGIController):
    def _setup(self):
        """Do basic request setup"""
        if pylons.session.get('logged_in', False):
            user = Human.load(self.db, pylons.session.get('user_id'))
            if not user or user.session_id != pylons.session.id:
                user = None
                pylons.session['logged_in'] = False
                pylons.session.delete()
                pylons.session.save()
        else:
            user = None
        if user:
            tzinfo = user.timezone or UTC
        else:
            tzinfo = UTC
        if isinstance(tzinfo, basestring):
            tzinfo = timezone(tzinfo)
        langs = pylons.request.accept_language.best_matches() or ['en']
        locale = Locale.negotiate(langs, ['en', 'uk', 'ja'], sep='-')
        pylons.c._format = Format(locale, tzinfo=tzinfo)
        pylons.c._locale = locale
        pylons.c._tzinfo = tzinfo
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
