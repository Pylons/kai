<div class="yui-b content">
    <%
    if c.tracebacks:
        results = list(c.tracebacks)
    if c.reverse:
        results.reverse()
    %>
    % if c.tracebacks:
        ${widgets.pager(c.start, results, c.tracebacks.total_rows, 'created')}
        <h1>Posted Tracebacks</h1>
        
        % for traceback in results[:10]:
        <% frame = traceback.frames[-1] %>
        <div class="exception">
            <h2 class="exception"><a href="${url('traceback', id=traceback.id)}">\
                ${traceback.exception_type} : ${h.truncate(traceback.exception_value, 140)}</a></h2>
            <div class="traceback_posted">
                <div class="traceback_gravatar">\
                    <img src="http://www.gravatar.com/avatar/${gravatar(traceback.email or 'anonymous')}?s=30">
                </div>
                <div class="user_data">
                    <div class="traceback_author">${traceback.displayname or 'Anonymous'}</div>\
                    ${widgets.format_timestamp(traceback.created)}
                </div>
                </div>
            <div class="exception_frame">
                <div class="frame">Last Frame:</div>
                <div class="moduleline">${frame.module}:\
                    <span class="lineno">${frame.line}</span>\
                    in ${frame.function}
                </div>
                ${highlight(frame.operation, py_lexer, html_formatter) | n}\
            </div>
        </div>
        % endfor
    % else:
    <h1>Posted Tracebacks</h1>
    
    <p>No tracebacks posted</p>
    % endif
</div>
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - Traceback Listing</%def>\
<%inherit file="../layout.mako" />\
<%!
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import md5
def gravatar(email):
    return md5.md5(email).hexdigest()

py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>