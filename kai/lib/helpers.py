"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
import datetime
import xml.utils.iso8601 as iso8601

from webhelpers.date import distance_of_time_in_words
from webhelpers.html.converters import textilize
from webhelpers.html.tags import link_to, select, stylesheet_link
from webhelpers.html.secure_form import auth_token_hidden_field
from webhelpers.text import truncate
from webhelpers.pylonslib import Flash as _Flash

from kai.lib.highlight import code_highlight


success_flash = _Flash('success')
failure_flash = _Flash('failure')

def load_stylesheet_assets():
    import pylons
    import os
    path = os.path.join(pylons.config['pylons.paths']['static_files'], 'css',
                        'CSSLIST')
    f = open(path,'r')
    stylesheets = f.read()
    f.close()
    return ['/css/%s.css' % f for f in stylesheets.split()]

def parse_iso_date(iso_date):
    return datetime.datetime.fromtimestamp(iso8601.parse(iso_date))
