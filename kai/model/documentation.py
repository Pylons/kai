import pylons
from couchdb.design import ViewDefinition

class Documentation(object):
    """Represents a project documentation doc
    
    The Documentation doc is project, version, and language specific
    and identified by its path as made by Sphinx.
    
    """
    by_path = ViewDefinition('documentation', 'by_path', '''
        function(doc) {
          if (doc.type == 'Documentation' && doc.current_page_name) {
            emit([doc.project, doc.version, doc.language, doc.current_page_name], null);
          }
        }''', include_docs=True)
    
    ids_for_version = ViewDefinition('documentation', 'ids_for_version','''
        function(doc) {
          if (doc.type == 'Documentation') {
            emit([doc.project, doc.version], {'_id': doc._id, '_rev': doc._rev});
          }
        }
        ''')
    
    doc_key = ViewDefinition('documentation', 'doc_key','''
        function(doc) {
          if (doc.type == 'Documentation') {
            emit([doc.filename, doc.version, doc.project], null);
          }
        }''', include_docs=True)
    
    @classmethod
    def fetch_doc(cls, project, version, language, path, **options):
        rows = cls.by_path(pylons.c.db, **options)[[project, version, language, path]]
        if len(rows) > 0:
            return list(rows)[0].doc
        else:
            return False
    
    @classmethod
    def delete_revision(cls, project, rev, **options):
        rows = cls.ids_for_version(pylons.c.db, **options)[[project, rev]]
        for row in rows:
            del pylons.c.db[row.id]
    
    @classmethod
    def exists(cls, doc, **options):
        key = [doc['filename'], doc['version'], doc['project']]
        rows = cls.doc_key(pylons.c.db, **options)[key]
        return len(rows) > 0
