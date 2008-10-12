<div class="yui-b">
    <h1>Snippet Repository</h1>
    <p>Pylons snippet repository is a place for pylites to share their code snippets with the community. Please only share fully functioning and tested snippets and include instructions so that novice and experienced Pylons users can benefit.</p>
    
	<form action="">
	<p>Title</p>
	<input type="text" name="title" value="" id="title" /><br />
	<br />
	<p>Description</p>
	<textarea name="description" id="description" style="width: 50em; height: 5em"></textarea><br />
	<br />
	<p>Code</p>
	<textarea name="content" id="content" style="width: 50em; height: 10em"></textarea><br />
	<br />
	<input type="submit" value="Add Snippet" />
	</form>
    
</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />