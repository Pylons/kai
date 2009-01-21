import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest
from tw.mods.pylonshf import validate

from kai.lib.base import BaseController, CMSObject, render
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
        redirect_to('paste', id=paste.id)
    
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
    
    def index(self, format='html', tag=None):
        """ Get the pasties by date and by author"""
        start = request.GET.get('start', '1')
        startkey = request.GET.get('startkey')
        prevkey = request.GET.get('prevkey')
        kwargs = {}
        if startkey:
            kwargs = dict(descending=True, startkey=startkey, count=11)
        elif prevkey:
            kwargs = dict(startkey=prevkey, count=11)
            c.reverse = True
        else:
            kwargs = dict(descending=True, count=11)
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
            c.total = list(Paste.all_tags(self.db)[tag])[0]['count']
        else:    
            c.pasties = Paste.by_time(self.db, **kwargs)
        c.start = start
        if format in ['atom', 'rss']:
            response.content_type = 'application/atom+xml'
            title = "PylonsHQ Pastie Feed"
            if tag:
                title += " - Tag: %s" % tag
            return render_feed(
                title=tag, link=url(qualified=True),
                description="Recent PylonsHQ pasties", objects=c.pasties[:10],
                pub_date='created')
        
        return render('/pasties/index.mako')
    
    def tagcloud(self):
        c.tag_sizes = Paste.tag_sizes()
        return render('/pasties/tagcloud.mako')
