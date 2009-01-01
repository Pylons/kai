import logging

from pylons import response, config, tmpl_context as c
from pylons.controllers.util import abort

# Monkey patch the lazywriter, since mercurial needs that on the stdout
import paste.script.serve as serve
serve.LazyWriter.closed = False

# Conditionally import the trac components in case things trac isn't installed
try:
    import os
    os.environ['TRAC_ENV_PARENT_DIR'] = '/usr/local/www'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(config['pylons.paths']['root'], 'egg_cache')
    import trac.web.main
    trac_app = trac.web.main.dispatch_request
    from trac.web import HTTPException
except:
    pass

from kai.lib.base import BaseController, render

log = logging.getLogger(__name__)

class TracsController(BaseController):
    def run_app(self, environ, start_response):
        if not trac_app:
            abort(404)
        if c.user:
            environ['REMOTE_USER'] = c.user.displayname
            environ['REMOTE_EMAIL'] = c.user.email
            environ['REMOTE_TZ'] = c.user.timezone
            environ['REMOTE_ID']= c.user.id
        try:
            return trac_app(environ, start_response)
        except HTTPException, obj:
            response.status_int = obj.code
            response.write(obj.message)
            return response(environ, start_response)
