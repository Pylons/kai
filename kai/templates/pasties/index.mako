<%
if c.pasties:
    results = list(c.pasties)
if c.reverse:
    pasties.reverse()
%>

${widgets.pager(c.start, results, c.pasties.total_rows, 'created')}
<h1>Pastes</h1>

<ul>
% for paste in results:
<li><a href="${url('paste', id=paste.old_id or paste.id)}">${paste.title}</a> - ${widgets.format_timestamp(paste.created)}</li>
% endfor
</ul>

<%namespace name="widgets" file="/widgets.mako" />
<%def name="title()">${parent.title()} - ${_('Pastebin')}</%def>
<%inherit file="layout.mako" />