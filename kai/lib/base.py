"""The base Controller API

Provides the BaseController class for subclassing.
"""
from paste.deploy.converters import asbool
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
import pylons

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        pylons.c.use_minified_assets = asbool(
            pylons.config.get('use_minified_assets', 'false'))
        return WSGIController.__call__(self, environ, start_response)
