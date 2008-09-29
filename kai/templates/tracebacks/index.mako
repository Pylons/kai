<div class="yui-b">
    <h1>List Tracebacks <span class="subtle">(${c.tracebacks.results})</span></h1>
    % for traceback in c.tracebacks.iterchildren(tag='traceback'):
    <% frame = traceback.last_frame %>\
    <h2 class="exception"><a href="${h.url_for('traceback', id=traceback.link.text.replace('.xml',''))}">\
        ${traceback.exception}</a></h2>
    <% date = h.parse_iso_date(traceback.created.text) %>\
    <p class="date">Posted on ${date.strftime('%Y-%m-%d at %H:%M:%S')}</p>
    <p class="moduleline">${frame.module}:\
    <span class="lineno">${frame.line}</span>\
     in ${frame.function}:<p>
    % if hasattr(frame, 'operation'):
    ${highlight(frame.operation.text, py_lexer, html_formatter) | n}\
    % endif
    % endfor
</div>
<%def name="title()">${parent.title()} - Traceback Listing</%def>\
<%inherit file="../layout.mako" />\
<%!
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>