${widgets.user_post(h.link_to(c.snippet.displayname, url=url('snippet_author', id=c.snippet.displayname)), 
                    c.snippet.email or 'anonymous', c.snippet.created, extra_classes='header')}
<h1>${c.snippet.title}</h1>

<div class="tag">Tags: <Span style="taglist">\
% for tag in c.snippet.tags:
    <a href="${url(controller='snippets', action='by_tag', tag=tag.strip())}">${tag}</a>\
% endfor
</span></div>

<div class="description">${c.snippet.description|n}</div>

<div class="snippet_content">${c.snippet_content|n}</div>

${widgets.show_comments(c.snippet.id)}
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('View Snippet: %s' % c.snippet.title)}</%def>
<%inherit file="layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def> 
<%def name="javascript()">
${parent.javascript()}
<script>
$(document).ready(function() {
    ${widgets.comment_js(c.snippet.id)}
});
</script>
</%def>