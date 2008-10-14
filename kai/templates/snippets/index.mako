<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>

<div class="yui-b content">
	<div class="relnav" id="relnav">
		<a href="${url('snippet_add')}">Add Snippet</a> | <a href="#">View By Rating</a> | <a href="${url(controller='snippets', action='by_author')}">View By Author</a> | <a href="#">Search</a>
	</div>
    <h1>Snippet Repository</h1>
    <p>Pylons snippet repository is a place for pylites to share their code snippets with the community. Please only share fully functioning and tested snippets and include instructions so that novice and experienced Pylons users can benefit.</p>
    
	<h1>Latest Snippets</h1>
	<ul>
	% for snippet in c.snippets:
	<li><a href="${url(controller='snippets', action='view', id=snippet.slug)}">${snippet.title}</a> - ${snippet.created.strftime('%m/%d/%Y %H:%M:%S')}</li>
	% endfor
    </ul>

	<h1>Latest Authors</h1>
	<ul>
	% for author in c.unique_authors:
	<li><a href="${url(controller='snippets', action='by_author', id=author[1])}">${author[0]}</a></li>
	% endfor
    </ul>

</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />