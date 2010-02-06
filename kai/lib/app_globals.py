"""The application's Globals object"""
from datetime import datetime
import md5
import os

from openid.server import server
from openid.store import filestore
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """
    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        oid_store = os.path.sep.join([config['pylons.cache_dir'], 'openid'])
        self.openid_store = filestore.FileOpenIDStore(oid_store)
        self.openid_server = server.Server(self.openid_store, config['openid.base_url'])
        
        self.etag_id = md5.md5(str(datetime.now().timetuple()[3])).hexdigest()
        self.versions = ['0.8','0.8.1', '0.8.2', '0.9', '0.9.1', '0.9.2', 
                         '0.9.3', '0.9.4', '0.9.4.1', '0.9.5', '0.9.6', '0.9.6.1',
                         '0.9.6.2', '0.9.7rc4', '0.9.7rc5', '0.9.7rc6', '0.9.7',
                         '0.10b1', '1.0b1', '1.0']
        self.current_version = '0.9.7'
        self.doc_version = '0.9.7'
