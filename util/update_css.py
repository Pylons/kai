from datetime import datetime
import re
import os
import sys


def compress_css(css):
    # remove comments - this will break a lot of hacks :-P
    css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", css ) # preserve IE<6 comment hack
    css = re.sub( r'/\*[\s\S]*?\*/', "", css )
    css = css.replace( "$$HACK1$$", '/**/' ) # preserve IE<6 comment hack

    # url() doesn't need quotes
    css = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', css )

    # spaces may be safely collapsed as generated content will collapse them anyway
    css = re.sub( r'\s+', ' ', css )

    # shorten collapsable colors: #aabbcc to #abc
    css = re.sub( r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css )

    # fragment values can loose zeros
    css = re.sub( r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css )
    
    total_css = []
    for rule in re.findall( r'([^{]+){([^}]*)}', css ):

        # we don't need spaces around operators
        selectors = [re.sub( r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip() ) for selector in rule[0].split( ',' )]

        # order is important, but we still want to discard repetitions
        properties = {}
        porder = []
        for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
            key = prop[0].strip().lower()
            if key not in porder: porder.append( key )
            properties[ key ] = prop[1].strip()

        # output rule if it contains any declarations
        if properties:
            total_css.append("%s{%s}" % ( ','.join( selectors ), ''.join(['%s:%s;' % (key, properties[key]) for key in porder])[:-1] ))
            #print "%s{%s}" % ( ','.join( selectors ), ''.join(['%s:%s;' % (key, properties[key]) for key in porder])[:-1] )
    return '\n'.join(total_css)


if len(sys.argv) < 2:
    print "Must have at least 1 argument:"
    print "\tpython update_css.py CONFIG.INI"
    sys.exit(0)

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(here_dir)
css_dir = os.path.join(conf_dir, 'kai', 'public', 'css')

ini_name = sys.argv[1]
ini_file = open(os.path.join(conf_dir, ini_name)).readlines()
csslist = open(os.path.join(css_dir, 'CSSLIST')).read()

# Combine all the CSS into one string
combined_css = ''
for f in csslist.split(' '):
    css_file = open(os.path.join(css_dir, '%s.css' % f)).readlines()
    parsed_css = ''
    for line in css_file:
        if line.startswith('@charset'):
            continue
        parsed_css += line
    combined_css += parsed_css

# Parse the CSS and turn on minification
sheet = compress_css(combined_css)

# Find the file we're going to write it out to
now = datetime.now()
fname = now.strftime('%m%d%Y')
file_name = fname
for x in range(1,30):
    exists = False
    file_name = 'phq-%s.%s-min.css' % (fname, x)
    try:
        stats = os.stat(os.path.join(css_dir, file_name))
        exists = True
    except OSError:
        pass
    if not exists:
        break

# Write it to the file
new_file = open(os.path.join(css_dir, file_name), 'w')
new_file.write(sheet)
new_file.close()

# Update the ini file to use the new minified CSS
new_ini = ''
for line in ini_file:
    if line.startswith('phq.minified_css ='):
        new_line = 'phq.minified_css = %s\n' % file_name
    else:
        new_line = line
    new_ini += new_line

nf = open(os.path.join(conf_dir, ini_name), 'w')
nf.write(new_ini)
