<div class="yui-b content">
    <div class="relnav" id="relnav">\
        ${h.link_to(_('Pastebin Home'), url=url('snippet_home'))} |
        % if c.user:
        ${h.link_to(_('New Paste'), url=url('paste_new'))} | \
        % endif
        ${h.link_to(_('View By Tag'), url=url('pasties_tagcloud'))}
    </div>
    ${next.body()}
</div>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
