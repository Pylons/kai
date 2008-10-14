<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def> 

<div class="yui-b content">
	<div class="relnav" id="relnav">
		<a href="${url('snippet_add')}">Add Snippet</a> | <a href="${url('report_snippet')}">Report Snippet</a> | <a href="#">View By Rating</a> | <a href="#">View By Author</a> | <a href="#">Search</a>
	</div>
    <h1>${c.snippet.title}</h1>
	
    <p>${c.snippet.description|n}</p>
	<p>${c.snippet_content|n}</p>
	<p>
	<h5>Author: <a href="${url(controller='snippets', action='by_author', id=c.snippet.human_id)}">${c.snippet.username}</a></h5>
	<h5>Tags: 
	% for tag in c.snippet.tags:
		<a href="${url(controller='snippets', action='by_tag', tag=tag.strip())}">${tag}</a>
	% endfor
	</h5>
	</p>
</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />