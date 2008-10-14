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
		<li><a href="${url(controller='snippets', action='by_author', id=author.key[1])}">${author.key[0]}</a> - ${author.value} snippets</li>
	% endfor
	</ul>
	% endif 
	
	% if c.snippets:
	<h1>View Snippets for ${c.username}</h1>
	<ul>
	% for snippet in c.snippets:
		<li><a href="${url('snippet_view', id=snippet.slug)}">${snippet.title}</a> - ${snippet.created.strftime('%m/%d/%Y %H:%M:%S')}</li>
	% endfor 
	</ul>
	% endif
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />