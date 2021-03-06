"""The base Controller API

Provides the BaseController class for subclassing.
"""
from babel import Locale, UnknownLocaleError
from babel.support import Format
from babel.util import UTC
from couchdb import Database
from paste.deploy.converters import asbool
from pylons.controllers import WSGIController
from pylons.controllers.util import abort
from pylons.i18n import add_fallback, get_lang, set_lang
from pylons.templating import render_mako
from pytz import timezone
import simplejson as json
import pylons

from kai.lib.helpers import success_flash
from kai.model import Human, Comment

def render(template_name, **kwargs):
    """Render override that add's babel objects"""
    extra_vars = kwargs.pop('extra_vars', {})
    c = pylons.tmpl_context._current_obj()
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
        locale = Locale.negotiate(langs, ['en', 'uk', 'ja'], sep='-') or Locale('en')
        pylons.tmpl_context._format = Format(locale, tzinfo=tzinfo)
        pylons.tmpl_context._locale = locale
        pylons.tmpl_context._tzinfo = tzinfo
        pylons.tmpl_context.user = user
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        pylons.tmpl_context.db = self.db = Database(pylons.config['couchdb_uri'])
        self._setup()
        
        pylons.tmpl_context.use_minified_assets = asbool(
            pylons.config.get('use_minified_assets', 'false'))
        return WSGIController.__call__(self, environ, start_response)


class CMSObject(object):
    """Provides common methods for CMS style objects like a blog entry,
    snippet, traceback, etc.
    
    Note that this requires the controller class to have a '_cms_object'
    attribute that points to the proper model for it.
    
    """
    def _check_owner(self, obj, user, check_session=False):
        if user and obj.human_id and user.id == obj.human_id:
            return True
        elif user and user.in_group('admin'):
            return True
        else:
            if check_session:
                if pylons.session.id and getattr(obj, 'session_id', None) and pylons.session.id == obj.session_id:
                    return True
            return False
        
    def delete(self, id):
        cms_object = self._cms_object.load(self.db, id) or abort(404)
        if self._check_owner(cms_object, pylons.tmpl_context.user, check_session=True):
            comments = list(Comment.by_time(self.db, startkey=[cms_object.id], endkey=[cms_object.id, {}]))
            update_seq = []
            for comment in comments:
                update_seq.append({'_id':comment.id, '_rev':comment.rev, '_deleted':True})
            update_seq.append({'_id':cms_object.id, '_rev':cms_object.rev, '_deleted':True})
            self.db.update(update_seq)
            success_flash('%s deleted' % cms_object.__class__.__name__)
        else:
            abort(401)


# Monkey patch httplib to buffer
import httplib
class HTTPResponse(httplib.HTTPResponse):
    def __init__(self, sock, **kw):
        httplib.HTTPResponse.__init__(self, sock, **kw)
        self.fp = sock.makefile('rb') 
httplib.HTTPConnection.response_class = HTTPResponse
