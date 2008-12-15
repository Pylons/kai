<h1>${_('All Tags')}</h1>

<div class="tagcloud">
    % for tag in c.tag_sizes:
        <span style="font-size: ${tag[2] * 1.3}px;">${h.link_to(tag[0], url=url('snippet_tag', tag=tag[0]))}</span> 
    % endfor
</div>
<%def name="title()">${parent.title()} - ${_('All Tags')}</%def>
<%inherit file="layout.mako" />