<%!
from datetime import datetime
from md5 import md5
import pytz

from kai.model import Comment, forms

%>
<%def name="show_comments(doc_id, poster_id=None, message=None)">
<%
total = Comment.total_comments(doc_id)
if total > 0:
    comments = list(Comment.by_time(c.db, startkey=[doc_id], endkey=[doc_id, {}]))
else:
    comments = []
%>
<div class="comments">
    <a name="comments"></a>
    <h2>Comments <span class="subtle">(${total})</span></h2>
    % for comment in comments:
        ${show_comment(comment, extra_class=(poster_id and poster_id == comment.human_id and 'highlight'))}
    % endfor
    
    % if message:
    <p class="suggest_comment">${message}</p>        
    % endif
    % if c.user:
        <div style="display: none;" id="comment_preview">&nbsp;</div>
        <div class="comment_format">${h.link_to('Formatting Quick Reference', url="http://hobix.com/textile/quick.html")}</div>
        ${forms.comment_form(action='#') | n}
    % else:
        <p>You must ${h.link_to(_('login'), url=url('account_login', redir=url.current()))} before you can comment.</p>
    % endif
</div>
</%def>
##
<%def name="show_comment(comment, extra_class=None)">
<div class="comment ${extra_class or ''}">
    ${user_post(comment.displayname, comment.email, comment.created, 'comments')}
    % if c.user and c.user.in_group('admin'):
    <div class="comment_delete commentid_${comment.id}">${h.link_to('Delete this comment', url='#', id_='comment_delete')}</div>
    % endif
    <div class="content">${h.textilize(comment.content)}</div>
</div>
</%def>
##
<%def name="user_post(displayname, email, post_date, extra_classes='')">
<div class="${extra_classes} user_post">
    <div class="user_icon">\
        % if email:
            <img src="http://www.gravatar.com/avatar/${md5(email).hexdigest()}?s=40">
        % else:
            <img src="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?s=40">
        % endif
    </div>
    <div class="username">${displayname or 'Anonymous'}</div>
    <div class="posted">${format_timestamp(post_date)}</div>
</div>
</%def>
##
<%def name="format_timestamp(date)">
<%
    diff = datetime.utcnow() - date
    date = timezone.localize(date)
    now = timezone.localize(datetime.utcnow())
%>
% if diff.days < 3:
${h.distance_of_time_in_words(date, now, granularity='minute')} ago
% else:
${format.datetime(date)}
% endif
</%def>
##
<%def name="comment_js(doc_id)">
$('input#comment_form_preview').click(function() {
    var content = $('#comment_form_comment')[0].value;
    var preview_url = '${url('preview_comment')}';
    $.ajax({
        data: {content:content},
        type: "POST",
        url: preview_url,
        success: function(data, textStatus) {
            $('#comment_preview').html(data).slideDown();
        }
    });
    return false;
});
$('input#comment_form_submit').click(function() {
    var content = $('#comment_form_comment')[0].value;
    var submit_url = '${url('post_comment', doc_id=doc_id)}';
    $.ajax({
        data: {content:content},
        type: "POST",
        url: submit_url,
        success: function(data, textStatus) {
            window.location = location.pathname;
        }
    });
    return false;
});
% if c.user and c.user.in_group('admin'):
$('div.comment_delete a').click(function() {
    var answer = window.confirm("Are you sure you want to delete this comment?");
    var delete_url = '/comment/' + $(this).parent().attr('class').replace(/^.*commentid_(\w*)$/,'$1');
    if (answer) {
        $.ajax({
            data: {'_method':'DELETE'},
            type: "POST",
            url: delete_url,
            success: function(data, textStatus) {
                window.location = location.pathname;
            }
        });
    }
    return false;
});
% endif
</%def>
##
<%def name="pager(start, lst, total, keyname)">
<%
    start = int(start)
    if total < start + 9:
        end = total
    else:
        end = start + 9
    startkey = lst[-1]._data[keyname]
    if start > 10:
        prevkey = lst[0]._data[keyname]
%>
<div id="paging">\
    <div class="pger">
    % if start > 10:
    <a class="prev" href="${url.current(start=start-10, prevkey=prevkey)}">← Previous Page</a> | 
    % else:
    <a class="prev">← Previous Page</a> | 
    % endif
\
    % if start + 9 < total:
    <a class="next" href="${url.current(start=start+10, startkey=startkey)}">Next Page →</a>
    % else:
    <a class="next">Next Page →</a>
    % endif
    </div>
    <div class="showing">Showing ${start}-${end} of ${total}</div>
</div>
</%def>
