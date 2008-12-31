"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

wiki = 'http://wiki.pylonshq.com'

def article_expand(kwargs):
    if 'article' not in kwargs:
        return kwargs
    article = kwargs.pop('article')
    kwargs['year'] = article.published.year
    kwargs['month'] = article.published.month
    kwargs['slug'] = article.slug
    return kwargs


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

    # Home url's
    map.connect('home', '/', controller='home', action='index')
    map.connect('features', '/features', controller='home', action='features')
    map.connect('history', '/history', controller='home', action='history')
    
    # Blog url's
    map.connect('article_archives', '/articles/archives/{year:\d+}/{month:\d+}/{slug}',
                controller='articles', action='archives', _filter=article_expand)
    map.resource('article', 'articles')
    
    # Code url's
    map.connect('buildbot', '/buildbot/{action}', controller='buildbot')
    
    # Doc url's
    map.connect('doc_upload', '/docs/upload', controller='docs', action='upload')
    map.connect('doc_upload_image', '/docs/upload_image', controller='docs', action='upload_image')
    map.connect('doc_delete', '/docs/delete_revision/{project}/{version}', controller='docs', action='delete_revision')
    map.redirect('/docs/{version}', '/docs/en/{version}/')
    map.connect('doc_home', '/docs/{language}/{version}/', controller='docs', action='view', url='index', language='en',
                version=globs.doc_version)
    map.connect('doc_view', '/docs/{language}/{version}/{url:.*}', controller='docs', action='view', language='en', 
                version=globs.doc_version)
    
    map.connect('wiki', 'http://wiki.pylonshq.com/', _static=True)
    map.connect('download', '/download/{version}', controller='download',
                action='index', version=version)
    map.connect('/download', controller='download', action='index', version=version)
    map.connect('cdocs', '%s/display/pylonsdocs/{page}' % wiki, _static=True)
    
    # Accounts
    map.connect('account_login', '/accounts/login', controller='accounts', action='login')
    map.connect('account_register', '/accounts/register', controller='accounts', action='register')
    map.connect('account_logout', '/accounts/logout', controller='accounts', action='logout')
    map.connect('verify_email', '/accounts/verify_email/{token}', controller='accounts', action='verify_email')
    map.connect('forgot_password', '/accounts/forgot_password', controller='accounts', action='forgot_password')
    map.connect('reset_password', '/accounts/reset_password/{token}', controller='accounts', action='change_password')
    
    # OpenID URL's
    map.connect('openid_associate', '/accounts/openid/associate', controller='accounts', action='openid_associate')
    map.connect('openid_register', '/accounts/openid/register', controller='accounts', action='openid_register')
    map.connect('openid_login', '/accounts/openid/login', controller='consumer', action='login')
    map.connect('openid_process', '/accounts/openid/process', controller='consumer', action='process')
    map.connect('openid_create', '/accounts/openid/create', controller='consumer', action='create')
    
    # Snippets
    map.connect('snippet_home', '/snippets', controller='snippets', action='index')
    map.connect('snippet_add', '/snippets/add', controller='snippets', action='add')
    map.connect('snippet_view', '/snippets/view/{id}', controller='snippets', action='view')
    map.connect('snippet_author', '/snippets/by_author/{id}', controller='snippets', action='by_author')
    map.connect('snippet_tag', '/snippets/by_tag/{tag}', controller='snippets', action='by_tag')
    map.connect('snippet_tagcloud', '/snippets/tagcloud', controller='snippets', action='tagcloud')
    
    # Pastebin
    map.connect('pasties_tagcloud', '/pasties/tagcloud', controller='pasties', action='tagcloud')
    map.connect('pasties_tag', '/pasties/by_tag/{tag}', controller='pasties', action='index')
    map.connect('pasties_author', '/pasties/by_author/{author}', controller='pasties', action='by_author')
    map.resource('paste', 'pasties')

    # Resources
    map.resource('traceback', 'tracebacks', member={'reown':'GET'})
    
    # Comments
    map.connect('preview_comment', '/comment/preview', controller='comments', action='preview', conditions=dict(method='POST'))
    map.connect('post_comment', '/comment/{doc_id}', controller='comments', action='create', conditions=dict(method='POST'))
    map.connect('delete_comment', '/comment/{id}', controller='comments', action='delete', conditions=dict(method='DELETE'))
    
    # Trac
    map.connect('/project/*path_info', controller='tracs', action='run_app')
    map.connect('trac_link', '/project/pylonshq/*url')
    
    # External Links
    map.connect('sqlalchemy', 'http://sqlalchemy.org/', _static=True)
    map.connect('sqlobject', 'http://www.sqlobject.org/', _static=True)
    map.connect('python-couchdb', 'http://code.google.com/p/couchdb-python/', _static=True)
    map.connect('formalchemy', 'http://code.google.com/p/formalchemy/', _static=True)
    map.connect('mako', 'http://makotemplates.org/', _static=True)
    map.connect('pylons_book', 'http://pylonsbook.com/', _static=True)

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
