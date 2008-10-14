"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map(globs=None):
    """Create, configure and return the routes Mapper"""
    version = config['pylons.app_globals'].current_version
    static_host = config['cdn.uri']

    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    
    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    map.connect('home', '/', controller='home', action='index')
    map.connect('buildbot', '/buildbot/{action}', controller='buildbot')
    
    # Doc url's
    map.connect('doc_upload', '/docs/upload', controller='docs', action='upload')
    map.connect('doc_upload_image', '/docs/upload_image', controller='docs', action='upload_image')
    map.redirect('/docs/{version}', '/docs/{version}/')
    map.connect('doc_home', '/docs/{version}/', controller='docs', 
                action='view', url='index', version=globs.doc_version)
    map.connect('doc_view', '/docs/{version}/{url:.*}', controller='docs',
                action='view', version=globs.doc_version)
    
    map.connect('wiki', 'http://wiki.pylonshq.com/', _static=True)
    map.connect('download', '/download/{version}', controller='download', action='index', 
                version=version)
    
    # Accounts
    map.connect('account_login', '/account/login', controller='accounts', action='login')
    map.connect('account_register', '/account/register', controller='accounts', action='register')
    
    # Snippets
    map.connect('snippet_home', '/snippets', controller='snippets', action='index')
    map.connect('snippet_add', '/snippets/add', controller='snippets', action='add')
    map.connect('snippet_view', '/snippets/view/{id}', controller='snippets', action='view')
    map.connect('/snippets/by_tag/{tag}', controller='snippets', action='by_tag')
    
    # Resources
    map.resource('traceback', 'tracebacks', member={'reown':'GET'})

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
