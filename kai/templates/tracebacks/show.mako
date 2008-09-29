<div class=”yui-b”>
    <h1>Exception ID: ${c.id}</h1>
    <% date = h.parse_iso_date(c.traceback.created.text) %>
    <p class="posted">Posted on ${date.strftime('%Y-%m-%d at %H:%M:%S')}</p>
    <% exc = c.traceback.traceback.exception %>\
    <div class="details">
    Exception: <span class="errormsg">${exc.type}: ${exc.value}</span>
    </div>
    <h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
    <div class="traceback">
        <ul>
        % for frame in c.traceback.traceback.stack.iterchildren(tag='frame'):
        <li><h4>
            Module <cite>${frame.module}</cite>, line <em>${frame.line}</em>, in \
<code>${frame.function}</code></h4>
            % if hasattr(frame, 'operation'):
            ${highlight(frame.operation.text, py_lexer, html_formatter) | n}\
            % else:
            No operation context
            % endif
        </li>
        % endfor
        </ul>
        <blockquote>${exc.type}: ${exc.value}</blockquote>
    </div>
    <div class="stats">
        <h2 class="system">System Info</h2>
        <div class="system">
            <% sysinfo = c.traceback.traceback.sysinfo %>
            ${sysinfo.language}: ${sysinfo.language.get('version')}
        </div>
        <div class="libraries">
            <h3 class="libraries">Libraries</h3>
            % for lib in sysinfo.libraries.iterchildren(tag='library'):
            <div class="library">
                ${lib.get('name')}: <span class="version">${lib.get('version')}</span>
            </div>
            % endfor
        </div>
    </div>
    
</div>
<%def name="title()">${parent.title()} - Traceback ${c.id}</%def>\
<%inherit file="../layout.mako" />\
<%!
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>