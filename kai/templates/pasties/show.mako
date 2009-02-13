<%!
from kai.lib.highlight import langdict
%>
% if c.paste.old_poster or not c.paste.email:
${widgets.user_post(c.paste.old_poster, 'anonymous', c.paste.created, extra_classes='header')}
% else:
${widgets.user_post(h.link_to(c.paste.displayname, 
                              url=url('pasties_author', author=c.paste.displayname)), 
                    c.paste.email, c.paste.created, extra_classes='header')}
% endif
<h1>${c.paste.title}</h1>
% if c.is_owner or (c.user and c.user.in_group('admin')):
<div class="traceback_delete">${h.link_to('Delete', id_='delete_paste')}</div>
% endif
<div class="language">Language: <span style="lang">${langdict[c.paste.language]}</span></div>

<div class="tags">Tags: <span style="taglist">\
% for tag in c.paste.tags:
    <a href="${url('pasties_tag', tag=tag.strip())}">${tag}</a>\
% endfor
</span></div>

<div class="tablestop">
${h.code_highlight(c.paste) |n}
</div>

<p class="subtle">${h.link_to('Download', url=url('download_paste', id=c.paste.old_id or c.paste.id))}</p>

${widgets.show_comments(c.paste.id)}
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('View Paste: %s' % c.paste.title)}</%def>
<%def name="javascript()">
${parent.javascript()}
% if c.is_owner:
<script>
$(document).ready(function() {
    $('#delete_paste').click(function() {
        var answer = window.confirm("Are you sure you want to delete this paste?");
        if (answer) {
            $.ajax({
                data: {"_method":"DELETE"},
                type: "POST",
                url: location.pathname,
                success: function(data, textStatus) {
                    window.location = '/pasties';
                }
            });
        }
        return false;
    });
    ${widgets.comment_js(c.paste.id)}
});
</script>
% endif
</%def>
<%inherit file="layout.mako" />
