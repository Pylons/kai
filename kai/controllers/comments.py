import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako_def

from kai.lib.base import BaseController, render
from kai.lib.helpers import textilize
from kai.lib.serialization import render_feed
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
    
    def delete(self, id):
        if not c.user or not c.user.in_group('admin'):
            abort(401)
        
        # Ensure doc exists
        doc = self.db.get(id)
        if not doc:
            abort(404)
        
        # Make sure its a comment
        if not doc['type'] == 'Comment':
            abort(404)
        
        self.db.delete(doc)
        return ''
    
    def index(self, format='html'):
        if format == 'html':
            abort(404)
        elif format in ['atom', 'rss']:
            # Pull comments and grab the docs with them for their info
            comments = list(Comment.by_anytime(c.db, descending=True, limit=20))
            commentdata = []
            for comment_doc in comments:
                comment = {}
                displayname = comment_doc.displayname or 'Anonymous'
                comment['created'] = comment_doc.created
                id = comment_doc.id
                doc = c.db.get(comment_doc.doc_id)
                if doc['type'] == 'Traceback':
                    comment['title'] = '%s: %s' % (doc['exception_type'], doc['exception_value'])
                else:
                    comment['title'] = doc.get('title', '-- No title --')
                comment['type'] = doc['type']
                comment['link'] = render_mako_def(
                    '/widgets.mako', 'comment_link', title=comment['title'],
                    comment_id=comment_doc.id, doc=doc, type=doc['type'],
                    urlonly=True).strip()
                comment['doc_id'] = comment_doc.doc_id
                comment['description'] = textilize(comment_doc.content)
                commentdata.append(comment)
            response.content_type = 'application/atom+xml'
            return render_feed(
                title="PylonsHQ Comment Feed", link=url.current(qualified=True), 
                description="Recent PylonsHQ comments", objects=commentdata,
                pub_date='created')
            
