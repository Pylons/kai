<h1>${c.snippet.title}</h1>
<p>${c.snippet.description|n}</p>
<p>${c.snippet_content|n}</p>
<p>
<h5>Author: ${h.link_to(c.snippet.displayname, url=url('snippet_author', id=c.snippet.human_id))}</h5>
<h5>Tags: \
% for tag in c.snippet.tags:
    <a href="${url(controller='snippets', action='by_tag', tag=tag.strip())}">${tag}</a>\
% endfor
</h5>
</p>
<%def name="title()">${parent.title()} - ${_('View Snippet: %s' % c.snippet.title)}</%def>
<%inherit file="layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def> 
