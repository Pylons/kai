"""Pylons environment configuration"""
import os
from datetime import timedelta

from couchdb import Server, Database
from mako.lookup import TemplateLookup
from paste.deploy.converters import asbool
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
import webhelpers.pylonslib.secure_form as secure_form

import kai.lib.app_globals as app_globals
import kai.lib.helpers
from kai.config.routing import make_map

secure_form.token_key = 'authentication_token'

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='kai', paths=paths)

    config['pylons.app_globals'] = app_globals.Globals(config)
    config['routes.map'] = make_map(config)
    config['pylons.h'] = kai.lib.helpers
    config['pylons.strict_tmpl_context'] = False
    config['beaker.session.cookie_expires'] = timedelta(seconds=604800)

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', output_encoding='utf-8',
        imports=['from webhelpers.html import escape'],
        filesystem_checks=asbool(config['debug']),
        default_filters=['escape'])
    
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    
    # Setup the database connection
    config['kai.server'] = Server(config['couchdb_server'])
    config['kai.db'] = Database(config['couchdb_uri'])
    
    return config
