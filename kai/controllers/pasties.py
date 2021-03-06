import logging

from pylons import cache, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import rest

from kai.lib.base import BaseController, CMSObject, render
from kai.lib.decorators import validate
from kai.lib.helpers import success_flash
from kai.lib.serialization import render_feed
from kai.model import Paste, forms
from kai.model.generics import all_doc_tags

log = logging.getLogger(__name__)

class PastiesController(BaseController, CMSObject):
    _cms_object = Paste
    
    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Pastebin'
    
    @rest.dispatch_on(POST='_process_new')
    def new(self):
        c.tags = [row['name'] for row in list(all_doc_tags(self.db))]
        return render('/pasties/create.mako')
    
    @validate(form=forms.pastebin_form, error_handler='new')
    def _process_new(self):
        self.form_result.pop('notabot')
        paste = Paste(**self.form_result)
        if c.user:
            paste.human_id = c.user.id
            paste.email = c.user.email
            paste.displayname = c.user.displayname
        else:
            paste.session_id = session.id
        if 'tags' in self.form_result:
            paste.tags = self.form_result['tags'].replace(',', ' ').strip().split(' ')

        paste.store(self.db)
        redirect(url('paste', id=paste.id))
    
    def show(self, id):
        doc = Paste.load(self.db, id)
        if not doc:
            docs = list(Paste.by_old_id(self.db)[id])
            if not docs:
                abort(404)
            doc = docs[0]
        c.paste = doc
        c.is_owner = self._check_owner(doc, c.user, check_session=True)
        return render('/pasties/show.mako')
    
    def download(self, id):
        doc = Paste.load(self.db, id)
        if not doc:
            docs = list(Paste.by_old_id(self.db)[id])
            if not docs:
                abort(404)
            doc = docs[0]
        id = doc.old_id or doc.id
        response.content_type = 'text/plain'
        response.headers['Content-disposition'] = 'attachment; filename=paste_%s.txt' % id
        return doc.code
    
    def index(self, format='html', tag=None):
        """ Get the pasties by date and by author"""
        start = request.GET.get('start', '1')
        startkey = request.GET.get('startkey')
        prevkey = request.GET.get('prevkey')
        kwargs = {}
        if startkey:
            kwargs = dict(descending=True, startkey=startkey, limit=11)
        elif prevkey:
            kwargs = dict(startkey=prevkey, limit=11)
            c.reverse = True
        else:
            kwargs = dict(descending=True, limit=11)
        if tag:
            if startkey:
                kwargs['startkey'] = [tag, startkey]
                kwargs['endkey'] = [tag]
            elif prevkey:
                kwargs['startkey'] = [tag, prevkey]
                kwargs['endkey'] = [tag, {}]
            else:
                kwargs['startkey'] = [tag, {}]
                kwargs['endkey'] = [tag]
            c.pasties = Paste.by_tag_time(self.db, **kwargs)
            total_count = list(Paste.all_tags(self.db)[tag]) or 0
            if total_count:
                total_count = total_count[0]['count']
            c.total = total_count
        else:    
            c.pasties = Paste.by_time(self.db, **kwargs)
        c.start = start
        if format in ['atom', 'rss']:
            response.content_type = 'application/atom+xml'
            title = "PylonsHQ Pastie Feed"
            if tag:
                title += " - Tag: %s" % tag
            return render_feed(
                title=title, link=url.current(qualified=True),
                description="Recent PylonsHQ pasties", objects=c.pasties[:10],
                pub_date='created')
        
        return render('/pasties/index.mako')
    
    def tagcloud(self):
        c.tag_sizes = cache.get_cache('pasties.py_tagcloud').get_value(
            'tags', createfunc=lambda: Paste.tag_sizes(), expiretime=180)
        return render('/pasties/tagcloud.mako')
