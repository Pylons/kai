import logging
import os

from paste.urlparser import StaticURLParser
from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from kai.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DownloadController(BaseController):
    def index(self, version, file=None):
        if version not in app_globals.versions:
            abort(404)
        
        dldir = os.path.join(config['download_dir'], str(version))
        if not os.path.exists(dldir):
            abort(404)
        
        if file:
            fdir = os.path.join(dldir, file)
            if not os.path.exists(fdir):
                abort(404)
            dl_srv = StaticURLParser(dldir)
            request.environ['PATH_INFO'] = '/%s' % (file)
            return dl_srv(request.environ, self.start_response)
                
        
        files = os.listdir(dldir)
        files.sort()
        filelist = []
        use_cachefly = version == app_globals.current_version
        # use_cachefly = False
        for f in files:
            if f.startswith('.'):
                continue
            if use_cachefly:
                filelist.append('<li><a href="http://cdn.pylonshq.com/download/%s/%s">'
                                '%s</a></li>\n' % (version, f, f))
            else:
                filelist.append('<li><a href="/download/%s/%s">%s</a></li>\n' 
                                % (version, f, f))
        filelist = '<ul>\n'+''.join(filelist)+'</ul>\n'
        c.files = filelist
        return render('/download/index.mako')
