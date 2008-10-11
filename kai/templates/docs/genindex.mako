<div class="yui-b sphinx content">
    <h1>Index</h1>
    
    <%
        ind_len = len(c.doc['genindexentries']) - 1
    %>
    % for index, (key, dummy) in enumerate(c.doc['genindexentries']):
    <a href="#${key}"><strong>${key}</strong></a>
    % if index != ind_len:
    |
    % endif
    % endfor
    
    % for loc, (key, entries) in enumerate(c.doc['genindexentries']):
    <h2 id="${key}">${key}</h2>
    <table width="100%" class="indextable"><tr><td width="33%" valign="top">
    <dl>
    <%
        breakat = c.doc['genindexcounts'][loc] // 2
        numcols = 1
        numitems = 0
        length = len(c.doc['genindexcounts'])
    %>
    % for entryname, (links, subitems) in entries:
    <dt>
        % if links:
        <a href="${links[0]}">${entryname}</a>
            % for here, link in enumerate(links[1:]):
            , <a href="${link}">[${here+1}]</a>
            % endfor
        % else:
        ${entryname}
        % endif
    </dt>
    % if subitems:
        <dd><dl>
            % for subentryname, subentrylinks in subitems:
            <dt><a href="${subentrylinks[0]}">${subentryname}</a>\
                % for here, link in enumerate(subentrylinks[1:]):
, <a href="${link}">${here+1}</a>
                % endfor
            % endfor
        </dl></dd>
    % endif
    <% 
        numitems = numitems + 1 + len(subitems)
    %>
    % if numcols < 2 and numitems > breakat:
        <%
        numcols += 1
        %>
        </dl></td><td width="33%" valign="top"><dl>
    % endif
    % endfor
    </dl></td></tr></table>
    % endfor
</div>
<%def name="title()">${parent.title()} - Documentation - Index</%def>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>