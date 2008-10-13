<div class="yui-b">
    <h1>Snippet Repository</h1>
    <p>Pylons snippet repository is a place for pylites to share their code snippets with the community. Please only share fully functioning and tested snippets and include instructions so that novice and experienced Pylons users can benefit.</p>
    
	<h1>Latest Snippets</h1>
	<ul>
	% for test in c.snippets:
	<li><a href="${url(controller='snippets', action='view', id=test.title)}">${test.title}</a> - ${test.created.strftime('%m/%d/%Y %H:%M:%S')}</li>
	% endfor
    </ul>

	<h1>Latest Authors</h1>
	
	<h1>Latest Titles</h1>

</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />