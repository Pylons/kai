<%
file_content = None
try:
    try:
        file_content = open(c.url)
        doc_content = file_content.read()
    except:
        h.redirect_to('/')
finally:
    if file_content:
        file_content.close()

try:
    doc_content = doc_content.decode('utf-8')
except:
    doc_content = doc_content.decode('utf-8', 'ignore')
%>
<div class="yui-b sphinx content">
% if c.version < g.current_version:
<div class="admonition warning">
<p class="first admonition-title">Warning</p>
<p class="last">This documentation does not refer to the most recent version of Pylons. <a href="http://wiki.pylonshq.com/display/pylonsdocs/Home">Current Documentation</a></p>
</div>
% endif

${doc_content | n}
</div>
<%def name="title()">${parent.title()} - Docs</%def>
<%def name="nav()">Docs</%def>
<%inherit file="/layout.mako"/>
