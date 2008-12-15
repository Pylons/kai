<div class="yui-b content">
    <% combined_exc = '%s: %s' % (c.traceback.exception_type, c.traceback.exception_value) %>
    <div class="traceback_post user_post">
        <div class="user_icon">\
            % if c.author:
                <img src="http://www.gravatar.com/avatar/${c.author.email_hash()}?s=30">
            % else:
                <img src="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?s=30">
            % endif
        </div>
        <div class="username">${c.author.displayname if c.author else 'Anonymous'}</div>
        <div class="posted">${format.datetime(c.traceback.created)}</div>
    </div>
    <h1>${h.link_to(combined_exc, url=url.current())}</h1>
    <h2 class="traceback">Traceback <em>(most recent call last)</em></h2>
    <div class="traceback">
        <ul>
        % for frame in c.traceback.frames:
        <li><h4>
            Module <cite>${frame.module}</cite>, line <em>${frame.line}</em>, in \
<code>${frame.function}</code></h4>
            ${highlight(frame.operation, py_lexer, html_formatter) | n}\
        </li>
        % endfor
        </ul>
        <blockquote>${c.traceback.exception_type}: ${c.traceback.exception_value}</blockquote>
    </div>
    <div class="stats">
        <h2 class="system">System Info</h2>
        <div class="system">
            ${c.traceback.language}: ${c.traceback.version}
        </div>
        <div class="libraries">
            <h3 class="libraries">Libraries</h3>
            % for lib in c.traceback.libraries:
            <div class="library">
                ${lib.name}: <span class="version">${lib.version}</span>
            </div>
            % endfor
        </div>
    </div>
</div>
<%def name="title()">${parent.title()} - ${_('Traceback %s' % c.traceback.id)}</%def>\
<%inherit file="../layout.mako" />\
<%!
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>