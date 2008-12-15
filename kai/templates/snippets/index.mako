<h1>Snippet Repository</h1>
<p>Pylons snippet repository is a place for pylites to share their code snippets with the community. Please only share fully functioning and tested snippets and include instructions so that novice and experienced Pylons users can benefit.</p>

<h1>Latest Snippets</h1>
<ul>
% for snippet in c.snippets:
<li><a href="${url(controller='snippets', action='view', id=snippet.slug)}">${snippet.title}</a> - ${widgets.format_timestamp(snippet.created)}</li>
% endfor
</ul>

<h1>Latest Authors</h1>
<ul>
% for author in c.unique_authors:
    <li>${h.link_to(author, url=url('snippet_author', id=author))}</li>
% endfor
</ul>
<%namespace name="widgets" file="/widgets.mako" />
<%def name="title()">${parent.title()} - ${_('Snippet Home')}</%def>
<%inherit file="layout.mako" />