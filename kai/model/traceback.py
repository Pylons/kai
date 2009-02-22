from datetime import datetime

import pylons
from couchdb.schema import DateTimeField, DictField, Document, TextField, \
    ListField, FloatField, Schema, IntegerField, BooleanField, View

from kai.model.generics import Comment

class Traceback(Document):
    type = TextField(default='Traceback')
    human_id = TextField()
    displayname = TextField()
    email = TextField()
    uuid = TextField()
    session_id = TextField()
    created = DateTimeField(default=datetime.utcnow)    
    description = TextField()
    
    # Meta
    language = TextField()
    version = TextField()
    full_version = TextField()
    platform = TextField()
    libraries = ListField(DictField(Schema.build(
        name = TextField(),
        version = TextField()
    )))
    
    # Traceback stack / Exception
    frames = ListField(DictField(Schema.build(
        module = TextField(),
        line = IntegerField(),
        function = TextField(),
        operation = TextField()
    )))
    exception_type = TextField()
    exception_value = TextField()
    
    by_uuid = View('traceback', '''
        function(doc) {
          if (doc.type == 'Traceback' && doc.uuid) {
            emit(doc.uuid, null);
          }
        }''', include_docs=True)
    
    by_time = View('traceback', '''
        function(doc) {
          if (doc.type == 'Traceback') {
            emit(doc.created, null);
          }
        }''', include_docs=True)
    
    by_session_id = View('traceback', '''
        function(doc) {
          if (doc.type == 'Traceback' && doc.session_id) {
            emit(doc.session_id, null);
          }
        }''', include_docs=True)
    
    @classmethod
    def from_xml(cls, content):
        try:
            from lxml import objectify
        except ImportError:
            return False
        
        data = objectify.fromstring(content)
        tb = cls()
        
        # Add the session id if available, otherwise force a new session
        if not pylons.session.id:
            pylons.session.save()
        tb.session_id = pylons.session.id
        
        exc = data.exception
        tb.exception_type = exc.type.text
        tb.exception_value = exc.value.text
        
        # Add the meta data
        sysinfo = data.sysinfo
        tb.language = sysinfo.language.text
        tb.version = sysinfo.language.get('version')
        tb.full_version = sysinfo.language.get('full_version')
        
        tb.libraries = []
        for lib in sysinfo.libraries.iterchildren(tag='library'):
            tb.libraries.append(dict(name=lib.get('name'),
                                version=lib.get('version')))
        
        tb.frames = []
        for frame in data.stack.iterchildren(tag='frame'):
            fd = dict(module=frame.module.text, line=int(frame.line.text),
                      function=frame.function.text)
            if hasattr(frame, 'operation'):
                fd['operation'] = frame.operation.text
            else:
                fd['operation'] = 'No operation context'
            tb.frames.append(fd)
        return tb
    
    def is_owner(self, user, check_session=False):
        if user and self.human_id and user.id == self.human_id:
            return True
        else:
            if check_session:
                if pylons.session.id and self.session_id and pylons.session.id == self.session_id:
                    return True
            return False
    
    def comment_count(self):
        comments = Comment.comment_count(pylons.c.db)[self.id]
        if not comments:
            return 0
        else:
            return comments[0]
    
    @classmethod
    def associate_tracebacks(cls, user):
        db = pylons.c.db
        tracebacks = list(cls.by_session_id(db)[pylons.session.id])
        if tracebacks:
            for tb in tracebacks:
                try:
                    tb.session_id = None
                    tb.human_id = user.id
                    tb.displayname = user.displayname
                    tb.email = user.email
                    tb.store(db)
                except:
                    pass
