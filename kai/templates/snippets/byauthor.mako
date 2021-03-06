% if c.authors:
<h1>Author List</h1>
<ul>
% for author in c.authors:
    <li>${h.link_to(author['author'], url=url('snippet_author', id=author['author']))} - ${author['amount']} snippets</li>
% endfor
</ul>
% endif 

% if c.snippets:
<h1>View Snippets for ${c.username}</h1>
<ul>
% for snippet in c.snippets:
    <li>${h.link_to(snippet.title, url=url('snippet', id=snippet.slug))} - ${widgets.format_timestamp(snippet.created)}</li>
% endfor 
</ul>
% endif
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="layout.mako" />