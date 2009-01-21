<div class="yui-b content pastebin">
    <div class="relnav" id="relnav">\
        ${h.link_to(_('Pastebin Home'), url=url('pasties'))} |
        ${h.link_to(_('New Paste'), url=url('new_paste'))} | \
        ${h.link_to(_('View By Tag'), url=url('pasties_tagcloud'))}
    </div>
    ${next.body()}
</div>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.auto_discovery_link(url('formatted_pasties', format='atom', qualified=True), feed_type='atom', title='PylonsHQ Pasties Feed')}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
