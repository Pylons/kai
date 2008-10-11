<div class="yui-b content">
    <div class="relnav">
        % if c.doc.get('prev'):
        <a href="${c.doc['prev']['link']}">&laquo; ${c.doc['prev']['title']}</a> | 
        % endif
        <a href="">${c.doc['title']}</a>
        % if c.doc.get('next'):
        | <a href="${c.doc['next']['link']}">${c.doc['next']['title']} &raquo;</a>
        % endif
    </div>
    % if c.doc.get('prev', False):
        ${display_toc(c.doc)}
    % endif
    ${c.doc['body'] | n}
</div>
<%def name="title()">${parent.title()} - Documentation - ${c.doc['title']}</%def>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
<%def name="display_toc(doc)">
<div id="toc">
<h3>Table of Contents</h3>
${doc['toc']|n}
</div>
</%def>