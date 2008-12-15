<div class="yui-b content">
    <% combined_exc = '%s: %s' % (c.traceback.exception_type, c.traceback.exception_value) %>
    <h1>${h.link_to(combined_exc, url=url.current())}</h1>
    <div class="traceback_posted">\
        % if c.is_owner:
        <div class="traceback_delete">${h.link_to('Delete', id_='delete_traceback')}</div>
        % endif
        ${widgets.format_timestamp(c.traceback.created)} by
        <span class="traceback_author">${c.author.displayname if c.author else 'Anonymous'}</span>\
        </div>
    <div class="traceback">
        <% 
            sort = request.GET.get('sort')
            options = ['In Call Order', 'Reverse Call Order']
            if sort and sort not in options:
                sort = options[0]
        %>
        <div class="sort_order">${h.select('order', sort, options, id='sort_order',
            onchange="document.location='%s?sort=' + document.getElementById('sort_order').value" % url.current())}</div>
        <%
            if sort == options[1]:
                frames = c.traceback.frames[::-1]
            else:
                frames = c.traceback.frames
        %>
        % if sort == options[1]:
        <blockquote>${c.traceback.exception_type}: ${c.traceback.exception_value}</blockquote>
        % endif
        <ul>
        % for frame in frames:
        <li><h4>
            Module <cite>${frame['module']}</cite>, line <em>${frame['line']}</em>, in \
<code>${frame['function']}</code></h4>
            ${highlight(frame['operation'], py_lexer, html_formatter) | n}\
        </li>
        % endfor
        </ul>
        % if sort == options[0]:
        <blockquote>${c.traceback.exception_type}: ${c.traceback.exception_value}</blockquote>
        % endif
        <div class="description">
            <h2>Description</h2>
            <p>${c.traceback.description if c.traceback.description else 'No Description Entered'}</p>
        </div>
        <div class="sysinfo">
            <div class="language"><span class="language">${c.traceback.language}</span>: <span class="version">${c.traceback.version}</span></div>
            <table id="traceback_libs">
                <tbody>
                    <%
                        libs = sorted(list(c.traceback.libraries), lambda x,y: cmp(x.name, y.name))
                    %>
                    % for lib in libs:
                    <tr><td>${lib.name}</td><td class="version">${lib.version}</td></tr>
                    % endfor
                </tbody>
            </table>
        </div>
    </div>
</div>
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('Traceback %s' % c.traceback.id)}</%def>\
<%def name="javascript()">
${parent.javascript()}
<script>

</script>
</%def>
<%inherit file="../layout.mako" />\
<%!
from datetime import datetime
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
py_lexer = PythonLexer()
html_formatter = HtmlFormatter()
%>