<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>

<div class="yui-b content">
	<div class="relnav" id="relnav">
		<a href="${url('snippet_add')}">Add Snippet</a> | <a href="#">View By Rating</a> | <a href="${url(controller='snippets', action='by_author')}">View By Author</a> | <a href="#">Search</a>
	</div>
	
	% if c.authors:
    <h1>Author List</h1>
	<ul>
	% for author in c.authors:
	    <li>${h.link_to(author['author'], url=url('snippet_author', id=author['id']))} - ${author['amount']} snippets</li>
	% endfor
	</ul>
	% endif 
	
	% if c.snippets:
	<h1>View Snippets for ${c.username}</h1>
	<ul>
	% for snippet in c.snippets:
	    <li>${h.link_to(snippet.title, url=url('snippet_view', id=snippet.slug))} - ${format.datetime(snippet.created, "medium")}</li>
	% endfor 
	</ul>
	% endif
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />