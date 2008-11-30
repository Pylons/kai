import pylons

class Documentation(object):
    """Represents a project documentation doc
    
    The Documentation doc is project, version, and language specific
    and identified by its path as made by Sphinx.
    
    """
    @classmethod
    def fetch_doc(cls, project, version, language, path, **options):
        options['include_docs'] = True
        rows = pylons.c.db.view('documentation/by_path', **options)[[project, version, language, path]]
        if len(rows) > 0:
            return list(rows)[0].doc
        else:
            return False
    
    @classmethod
    def delete_revision(cls, project, rev, **options):
        rows = pylons.c.db.view('documentation/ids_for_version', **options)[[project, rev]]
        for row in rows:
            del pylons.c.db[row.id]
    
    @classmethod
    def exists(cls, doc, **options):
        key = [doc['filename'], doc['version'], doc['project']]
        rows = pylons.c.db.view('documentation/doc_key', group=True, **options)[key]
        return len(rows) > 0
