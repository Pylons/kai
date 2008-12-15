<%def name="user_post(user, post_date, extra_classes='')">
<div class="${extra_classes} user_post">
    <div class="user_icon">\
        % if user:
            <img src="http://www.gravatar.com/avatar/${user.email_hash()}?s=30">
        % else:
            <img src="http://www.gravatar.com/avatar/3b3be63a4c2a439b013787725dfce802?s=30">
        % endif
    </div>
    <div class="username">${user.displayname if user else 'Anonymous'}</div>
    <div class="posted">${format.datetime(post_date)}</div>
</div>
</%def>
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
<%!
from datetime import datetime
import pytz
%>