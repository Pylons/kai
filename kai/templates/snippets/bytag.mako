<h1>${_('Snippets for tag: %s' % c.tag)}</h1>
<ul>
% for snippet in c.snippets:
    <li>${h.link_to(snippet.title, url=url('snippet', id=snippet.slug))} - ${format.datetime(snippet.created, "medium")}</li>
% endfor 
</ul>
<%def name="title()">${parent.title()} - ${_('Snippets for tag: %s' % c.tag)}</%def>
<%inherit file="layout.mako" />