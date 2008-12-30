import logging

from pylons import config, tmpl_context as c
from pylons.controllers.util import abort

# Conditionally import the trac components in case things trac isn't installed
try:
    import os
    os.environ['TRAC_ENV_PARENT_DIR'] = '/usr/local/www'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join([config['pylons.paths']['root'], 'egg_cache'])
    import trac.web.main
    trac_app = trac.web.main.dispatch_request
except:
    trac_app = None

from kai.lib.base import BaseController

log = logging.getLogger(__name__)

class TracsController(BaseController):
    def run_app(self, environ, start_response):
        if not trac_app:
            abort(404)
        if c.user:
            environ['REMOTE_USER'] = c.user.displayname
        return trac_app(environ, start_response)