<h1>${c.paste.title}</h1>
<h5>Author: ${c.paste.old_poster or (c.paste.email and widgets.user_post(c.paste.displayname, c.paste.email, c.paste.created)) or c.paste.displayname}</h5>
<div class="tags">Tags: \
% for tag in c.paste.tags:
    <a href="${url('pasties_tag', tag=tag.strip())}">${tag}</a>\
% endfor
</div>
${h.code_highlight(c.paste) |n}
${widgets.show_comments(c.paste.id)}
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('View Paste: %s' % c.paste.title)}</%def>
<%inherit file="layout.mako" />
