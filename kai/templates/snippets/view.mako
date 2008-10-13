<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def> 

<div class="yui-b content">
<div class="yui-b">
    <h1>${c.snippet.title}</h1>
    <p>${c.snippet.description|n}</p>
	<p>${c.snippet.content|n}</p>

</div>
</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />