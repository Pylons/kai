"""Query and interact with the buildbot via XMLRPC for info"""
import xmlrpclib
from datetime import datetime

import pylons
from pytz import timezone

buildbot_server = xmlrpclib.Server(pylons.config['buildbot_server'])
day = 60 * 60 * 24

def recent_builds(num_builds=2):
    """Fetchs all builds for num_builds, and sorts them into
    an organized dict

    For performance, this function caches itself for 30 seconds at a
    time

    """
    mycache = pylons.cache.get_cache(__file__ + 'recent_builds')
    def get_items():
        results = buildbot_server.getAllLastBuilds(num_builds)
        builders = {}
        tzinfo = timezone('US/Pacific')
        for res in results:
            start = datetime.fromtimestamp(res[2], tzinfo)
            end = datetime.fromtimestamp(res[3], tzinfo)
            elapsed = res[3] - res[2]
            build = dict(name=res[0], version=res[1], 
                         start=start, end=end, branch=res[4],
                         revision=res[5], results=res[6], text=res[7],
                         reasons=res[8], elapsed=elapsed)
            builders.setdefault(build['name'], []).append(build)
        for ver, items in builders.items():
            builders[ver] = sorted(items, cmp=lambda x,y: cmp(y['end'], x['end']))
        return builders
    return mycache.get_value(key='', createfunc=get_items, expiretime=30)

def build_info(name, build_number):
    mycache = pylons.cache.get_cache(__file__ + 'build_info')
    if isinstance(build_number, basestring):
        build_number = int(build_number)
    def get_build():
        results = buildbot_server.getBuild(name, build_number)
        return results
    return mycache.get_value(key='%s%s' % (name, build_number), createfunc=get_build, expiretime=day)
