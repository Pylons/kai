import logging
import re

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest
from tw.mods.pylonshf import validate

from kai.lib.base import BaseController, render
from kai.lib.decorators import in_group
from kai.lib.helpers import failure_flash, success_flash
from kai.lib.serialization import render_feed
from kai.model.forms import new_article_form
from kai.model import Article

log = logging.getLogger(__name__)

class ArticlesController(BaseController):
    def __before__(self):
        c.active_tab = 'Community'
        c.active_sub = 'Blog'
    
    def index(self, format='html'):
        start = request.GET.get('start', '1')
        startkey = request.GET.get('startkey')
        prevkey = request.GET.get('prevkey')
        if startkey:
            c.articles = Article.by_time(self.db, descending=True, startkey=startkey, count=11)
        elif prevkey:
            c.articles = Article.by_time(self.db, startkey=prevkey, count=11)
            c.reverse = True
        else:
            c.articles = Article.by_time(self.db, descending=True, count=11)
        c.start = start
        
        if format == 'html':
            return render('/articles/index.mako')
        elif format in ['atom', 'rss']:
            response.content_type = 'application/atom+xml'
            return render_feed(
                title="PylonsHQ Article Feed", link=url(qualified=True), 
                description="Recent PylonsHQ articles", objects=c.articles,
                pub_date='published')
    
    def archives(self, year, month, slug):
        articles = list(Article.by_slug(c.db, include_docs=True)[(int(year), int(month), slug)]) or abort(404)
        c.article = articles[0]
        return render('/articles/show.mako')
    
    @in_group('admin')
    def new(self):
        return render('/articles/new.mako')
    
    @in_group('admin')
    @validate(form=new_article_form, error_handler='new')
    def create(self):
        result = self.form_result
        article = Article(title=result['title'], summary=result['summary'],
                          body=result['body'], published=result['publish_date'],
                          human_id=c.user.id, author=c.user.displayname)
        
        ## generate the slug
        slug = result['title'].replace(" ", "_")
        slug = slug.lower()
        slug = re.sub('[^A-Za-z0-9_]+', '', slug)
        article.slug = slug
        article.store(self.db)
        success_flash('Article saved and published')
        redirect_to('articles')
