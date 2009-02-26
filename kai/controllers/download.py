import logging
import os

from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DownloadController(BaseController):
    def index(self, version):
        if version not in app_globals.versions:
            abort(404)
        
        dldir = os.path.join(config['download_dir'], str(version))
        if not os.path.exists(dldir):
            abort(404)
        
        files = os.listdir(dldir)
        files.sort()
        filelist = []
        #use_cachefly = version == app_globals.current_version
        use_cachefly = False
        for f in files:
            if f.startswith('.'):
                continue
            if use_cachefly:
                filelist.append('<li><a href="http://pylons.cachefly.net/download/%s/%s">'
                                '%s</a></li>\n' % (version, f, f))
            else:
                filelist.append('<li><a href="/download/%s/%s">%s</a></li>\n' 
                                % (version, f, f))
        filelist = '<ul>\n'+''.join(filelist)+'</ul>\n'
        c.files = filelist
        return render('/download/index.mako')
