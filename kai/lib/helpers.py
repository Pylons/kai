"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
import datetime
import xml.utils.iso8601 as iso8601

from webhelpers.html.tags import link_to, stylesheet_link

def load_stylesheet_assets():
    import pylons
    import os
    path = os.path.join(pylons.config['pylons.paths']['root'], 'public', 
                        'css', 'CSSLIST')
    f = open(path,'r')
    stylesheets = f.read()
    f.close()
    return ['/css/%s.css' % f for f in stylesheets.split()]

def parse_iso_date(iso_date):
    return datetime.datetime.fromtimestamp(iso8601.parse(iso_date))
