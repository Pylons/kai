<div class="yui-b content snippets">
    <div class="relnav" id="relnav">\
        ${h.link_to(_('Snippet Home'), url=url('snippets'))} |
        % if c.user:
        ${h.link_to(_('Add Snippet'), url=url('new_snippet'))} | \
        % endif
        ${h.link_to(_('View By Author'), url=url(controller='snippets', action='by_author'))} | \
        ${h.link_to(_('View By Tag'), url=url('snippet_tagcloud'))}
    </div>
    ${next.body()}
</div>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
