import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.lib.buildbot import recent_builds, build_info

log = logging.getLogger(__name__)

class BuildbotController(BaseController):
    def __before__(self):
        c.active_tab = 'Code'
        c.active_sub = 'Buildbots'

    def index(self):
        builds = recent_builds(20)
        releases = {}
        dev = {}
        for ver in builds:
            if ver.startswith('Release'):
                releases[ver] = builds[ver]
            else:
                dev[ver] =  builds[ver]
        c.releases, c.dev = releases, dev
        return render('/buildbot/index.mako')
    
    def details(self, id):
        buildname, version = id.split('__')
        c.details = build_info(buildname, version)
        return render('/buildbot/details.mako')
