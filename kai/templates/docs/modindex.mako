<div class="yui-b sphinx content">
    <h1>Global Module Index</h1>
    
    <% 
        letter_length = len(c.doc['letters']) -1
    %>
    % for index, letter in enumerate(c.doc['letters']):
    <a href="#cap-${letter}"><strong>${letter}</strong></a>
        % if index != letter_length:
            |
        % endif
    % endfor
    
    <table width="100%" class="indextable" cellspacing="0" cellpadding="2">
    % for modname, collapse, cgroup, indent, fname, synops, pform, dep in c.doc['modindexentries']:
    % if not modname:
        <tr class="pcap"><td></td><td>&nbsp;</td><td></td></tr>
        <tr class="cap"><td></td><td><a name="cap-${fname}"><strong>${fname}</strong></a></td><td></td></tr>
    % else:
        % if indent:
            <tr class="cg-${cgroup}">
        % else:
            <tr>
        % endif
        <td>
            % if collapse:
            <img src="/images/minus.png" id="toggle-${cgroup}" class="toggler" style="display: none" />
            % endif
        </td>
        <td>
            % if indent:
                &nbsp;&nbsp;&nbsp;
            % endif
            % if fname:
                <a href="${fname}">
            % endif
            <tt class="xref">${modname}</tt>
            % if fname:
                </a>
            % endif
            % if len(pform) > 1 and pform[0]:
                <em>(${pform|join(', ')})</em>
            % endif
        </td>
        <td>
            % if dep:
            <strong>Deprecated</strong>
            % endif
            <em>${synops}</em>
        </td></tr>
    % endif
    % endfor
    </table>
</div>
<%def name="title()">${parent.title()} - Documentation - Module Index</%def>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>