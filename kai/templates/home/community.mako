
<div class="yui-gb content">
    <h2>Community Overview</h2>
    <p>Latest happenings from the Pylons community, mail lists, etc.</p>
    <div class="yui-u first">
        <h3>Snippets</h3>
        <div class="itemlist">
            % for snippet in c.snippets:
            <div class="result">
                ${h.link_to(snippet.title, url=url('snippet', id=snippet.slug))}
                <div class="blurb">
                ${h.truncate(snippet.description, length=90, whole_word=True)}
                </div>
                <div class="meta">${widgets.format_timestamp(snippet.created)} - ${snippet.displayname or 'Anonymous'}</div>
            </div>
            % endfor
        </div>
    </div>
    <div class="yui-u">
        <h3>Pastes</h3>
        <div class="itemlist">
            % for paste in c.pastes:
            <div class="result">
                ${h.link_to(paste.title, url=url('paste', id=paste.old_id or paste.id))}
                <div class="blurb">
                    % if len(paste.tags) > 0:
                    <span class="tagheader">Tags: </span>\
                        % for tag in paste.tags:
                            % if tag:
                            ${h.link_to(tag, url=url('pasties_tag', tag=tag))} 
                            % endif
                        % endfor
                    % endif
                </div>
                <div class="meta">${widgets.format_timestamp(paste.created)} - ${paste.displayname or 'Anonymous'}</div>
            </div>
            % endfor
        </div>
    </div>
    <div class="yui-u">
        <h2>Mail List</h2>
        <div id="maillist" class="itemlist">
        </div>
    </div>
</div>
<%def name="title()">${parent.title()} - ${_('Community')}</%def>
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="javascript()">
${parent.javascript()}
<script type="text/javascript" src="/javascripts/community.js" charset="utf-8"></script>
</%def>
<%inherit file="/layout.mako" />
<%namespace name="widgets" file="/widgets.mako"/>
