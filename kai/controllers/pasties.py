import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.model import Paste

log = logging.getLogger(__name__)

class PastiesController(BaseController):
    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Pastebin'
    
    def show(self, id):
        doc = Paste.load(self.db, id)
        if not doc:
            abort(404)
        c.paste = doc
        return render('/pasties/show.mako')
    
    def index(self):
        """ Get the pasties by date and by author"""
        start = request.GET.get('start', '1')
        startkey = request.GET.get('startkey')
        prevkey = request.GET.get('prevkey')
        if startkey:
            c.pasties = Paste.by_time(self.db, descending=True, startkey=startkey, count=11)
        elif prevkey:
            c.pasties = Paste.by_time(self.db, startkey=prevkey, count=11)
            c.reverse = True
        else:
            c.pasties = Paste.by_time(self.db, descending=True, count=11)
        c.start = start
        return render('/pasties/index.mako')
    
    def by_tag(self, tag=None):
        """View pasties by a particular tag.
        
        Keyword arguments:
        tag - a tag (string)
        
        """
        c.pasties = list(Paste.by_tag(self.db)[tag]) or abort(404)
        c.tag = tag
        return render('/pasties/bytag.mako')

    def tagcloud(self):
        c.tag_sizes = Paste.tag_sizes()
        return render('/pasties/tagcloud.mako')
