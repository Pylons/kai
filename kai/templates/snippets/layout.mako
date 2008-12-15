<div class="yui-b content">
    <div class="relnav" id="relnav">\
        ${h.link_to('Snippet Home', url=url('snippet_home'))} |
        % if c.user:
        ${h.link_to('Add Snippet', url=url('snippet_add'))} | \
        % endif
        ${h.link_to('View By Author', url=url(controller='snippets', action='by_author'))}
    </div>
    ${next.body()}
</div>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
