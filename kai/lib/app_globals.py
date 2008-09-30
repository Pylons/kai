"""The application's Globals object"""
from datetime import datetime
import md5

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """
    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.etag_id = md5.md5(str(datetime.now().timetuple()[3])).hexdigest()
        self.versions = ['0.8','0.8.1', '0.8.2', '0.9', '0.9.1', '0.9.2', 
                         '0.9.3', '0.9.4', '0.9.4.1', '0.9.5', '0.9.6', '0.9.6.1',
                         '0.9.6.2', '0.9.7rc1']
        self.current_version = '0.9.7rc1'
