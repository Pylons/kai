import logging

from paste.script.util.uuid import uuid4
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from kai.lib.base import BaseController, CMSObject, render
from kai.lib.helpers import success_flash
from kai.model import Comment, Human, Traceback

log = logging.getLogger(__name__)

class TracebacksController(BaseController, CMSObject):
    _cms_object = Traceback
    
    def __before__(self):
        c.active_tab = 'Tools'
        c.active_sub = 'Tracebacks'
    
    def index(self):
        start = request.GET.get('start', '1')
        startkey = request.GET.get('startkey')
        prevkey = request.GET.get('prevkey')
        if startkey:
            c.tracebacks = Traceback.by_time(self.db, descending=True, startkey=startkey, count=11)
        elif prevkey:
            c.tracebacks = Traceback.by_time(self.db, startkey=prevkey, count=11)
            c.reverse = True
        else:
            c.tracebacks = Traceback.by_time(self.db, descending=True, count=11)
        c.start = start
        return render('/tracebacks/index.mako')
    
    @jsonify
    def create(self):
        """Create a new traceback in the system, pegged to the current
        user ID and session ID"""
        tb = Traceback.from_xml(request.body)
        tb.uuid = uuid4()
        tb.store(self.db)
        result = {}
        uuid = tb.uuid
        result['traceback'] = dict(link=tb.id, uuid=uuid)
        return result
    
    def reown(self, id):
        if 'uuid' not in request.GET:
            abort(500)
        tb = Traceback.load(self.db, id) or abort(404)
        session.save()
        if c.user:
            tb.displayname = c.user.displayname
            tb.human_id = c.user.id
            tb.email = c.user.email
        else:
            tb.session_id = session.id
        tb.uuid = None
        tb.store(self.db)
        return 'ok'
    
    def show(self, id):
        c.traceback = Traceback.load(self.db, id) or abort(404)
        if c.traceback.displayname:
            c.author = Human.load(self.db, c.traceback.human_id)
        c.is_owner = self._check_owner(c.traceback, c.user, check_session=True)
        return render('/tracebacks/show.mako')
