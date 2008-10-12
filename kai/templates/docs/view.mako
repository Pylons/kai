<div class="yui-b content">
    ${show_nav()}
    % if c.doc.get('prev', False):
        ${display_toc(c.doc)}
    % endif
    ${c.doc['body'] | n}
    ${show_nav()}
</div>
<%def name="title()">${parent.title()} - Documentation - ${c.doc['title']}</%def>
<%inherit file="../layout.mako" />
<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
</%def>
<%def name="show_nav()">
<div class="relnav">
    % if c.doc.get('prev'):
    <a href="${c.doc['prev']['link']}">&laquo; ${c.doc['prev']['title']|n}</a> | 
    % endif
    <a href="">${c.doc['title']|n}</a>
    % if c.doc.get('next'):
    | <a href="${c.doc['next']['link']}">${c.doc['next']['title']|n} &raquo;</a>
    % endif
</div>
</%def>
<%def name="javascript()">
${parent.javascript()}
<script>
$(function() {

  var
    toc = $('#toc').show(),
    items = $('#toc > ul').hide();

  $('#toc h3')
    .click(function() {
      if (items.is(':visible')) {
        items.animate({
          height:     'hide',
          opacity:    'hide'
        }, 300, function() {
          toc.removeClass('expandedtoc');
        });
      }
      else {
        items.animate({
          height:     'show',
          opacity:    'show'
        }, 400);
        toc.addClass('expandedtoc');
      }
    });

});
</script>
</%def>
<%def name="display_toc(doc)">
<div id="toc">
<h3>Table of Contents</h3>
<ul style="display:none">${doc['toc'][4:]|n}
</div>
</%def>