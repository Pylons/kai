<div class="yui-b content">
    <h1>List Tracebacks <span class="subtle">(${c.tracebacks.total_rows})</span></h1>
    <%
    results = list(c.tracebacks)
    if c.reverse:
        results.reverse()
    %>
    ${widgets.pager(c.start, results, c.tracebacks.total_rows, 'created')}
    % for traceback in results[:10]:
    <% frame = traceback.frames[-1] %>
    <div class="exception">
        <h2 class="exception"><a href="${url('traceback', id=traceback.id)}">\
            ${traceback.exception_type} : ${traceback.exception_value}</a></h2>
        <div class="traceback_posted">${widgets.format_timestamp(traceback.created)} by
            <span class="traceback_author">${traceback.displayname or 'Anonymous'}</span>\
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
</div>
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - Traceback Listing</%def>\
<%inherit file="../layout.mako" />\
<%!
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>