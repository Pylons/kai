<%
results = list(c.pasties)
if c.reverse:
    results.reverse()
total = c.total or c.pasties.total_rows
%>

% if results:
${widgets.pager(c.start, results, total, 'created')}
% endif
<h1>Pastes\
% if c.tag:
 <span class="subtle">(Viewing tag: ${c.tag})</span>\
% endif
</h1>

% for paste in results[:10]:
<div class="pastie">
    <h2 class="pastie">${h.link_to(paste.title, url=url('paste', id=paste.old_id or paste.id))}</h2>
    <div class="pastedata">
        <div class="language">Language: \
        % if paste.language:
        <span class="lang">${h.langdict[paste.language]}</span>\
        % else:
        No language provided\
        % endif
        </div>
        % if paste.tags:
        <div class="tags"><span class="tagheader">Tags: </span>\
            % for tag in paste.tags:
                % if tag:
                ${h.link_to(tag, url=url('pasties_tag', tag=tag))} 
                % endif
            % endfor
        </div>
        % endif
    </div>
    % if paste.old_poster or not paste.email:
    ${widgets.user_post(paste.old_poster, 'anonymous', paste.created, extra_classes='pastelist')}
    % else:
    ${widgets.user_post(paste.displayname, paste.email, paste.created, extra_classes='pastelist')}
    % endif
    <div class="clearfix">&nbsp;</div>
</div>
% endfor

<%namespace name="widgets" file="/widgets.mako" />
<%def name="title()">${parent.title()} - ${_('Pastebin')}</%def>
<%inherit file="layout.mako" />
<%def name="styles()">
% if c.tag:
${h.auto_discovery_link(url('formatted_pasties_tag', tag=c.tag, format='atom', qualified=True), feed_type='atom', title='PylonsHQ Pasties Feed')}
% else:
${h.auto_discovery_link(url('formatted_pasties', format='atom', qualified=True), feed_type='atom', title='PylonsHQ Pasties Feed')}
% endif
${parent.styles()}
</%def>