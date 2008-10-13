<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def> 

<div class="yui-b content">
    <h1>${c.snippet.title}</h1>
    <p>${c.snippet.description|n}</p>
	<p>${c.snippet_content|n}</p>
</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />