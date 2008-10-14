<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
<div class="yui-b content">
	<div class="relnav" id="relnav">
		<a href="#">View By Rating</a> | <a href="${url(controller='snippets', action='by_author')}">View By Author</a> | <a href="#">Search</a>
	</div>
    <h1>Snippet Repository</h1>
    <p>Pylons snippet repository is a place for pylites to share their code snippets with the community. Please only share fully functioning and tested snippets and include instructions so that novice and experienced Pylons users can benefit.</p>
	
	% if c.exists:
		<h3><span class="error-message">A snippet with that title already exists, please choose another title.</span></h3>
	% endif
	
	% if c.add_error:
		<h3><span class="error-message">An unknown error occurred when adding your snippet. ${c.error}</span></h3>
	% endif
	
	<form action="${url('snippet_add')}" method="POST">
	<p>Title</p>
	<input type="text" name="title" value="" id="title" /><br />
	<br />
	<p>Description</p>
	<textarea name="description" id="description" style="width: 50em; height: 5em"></textarea><br />
	<br />
	<p>Code</p>
	<textarea name="content" id="content" style="width: 50em; height: 10em"></textarea><br />
	<br />
	<p>Tags</p>
	<input type="text" name="tags" id="tags" value="" /><br />
	<br />
	<input type="submit" value="Add Snippet" />
	</form>

</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />