<%
results = list(c.pasties)
if c.reverse:
    results.reverse()
total = c.total or c.pasties.total_rows
%>

${widgets.pager(c.start, results, total, 'created')}
<h1>Pastes</h1>

<ul>
% for paste in results[:10]:
<li><a href="${url('paste', id=paste.old_id or paste.id)}">${paste.title}</a> - ${widgets.format_timestamp(paste.created)}</li>
% endfor
</ul>

<%namespace name="widgets" file="/widgets.mako" />
<%def name="title()">${parent.title()} - ${_('Pastebin')}</%def>
<%inherit file="layout.mako" />