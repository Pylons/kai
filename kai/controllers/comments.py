import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.lib.helpers import textilize
from kai.model import Comment

log = logging.getLogger(__name__)

class CommentsController(BaseController):
    def preview(self):
        data = request.POST['content']
        return textilize(data)
        
    def create(self, doc_id):
        if not c.user:
            abort(401)
        
        # Ensure the doc exists
        doc = self.db.get(doc_id)
        if not doc:
            abort(404)
        
        
        comment = Comment(doc_id=doc_id, displayname=c.user.displayname,
                          email=c.user.email, human_id=c.user.id,
                          content=request.POST['content'])
        comment.store(self.db)
        return ''
