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
%>
% if diff.days < 3:
${h.distance_of_time_in_words(date, granularity='minute')} ago
% else:
${format.datetime(date)}
% endif
</%def>
<%!
from datetime import datetime
%>