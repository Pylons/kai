<%!
    from kai.model.forms import new_article_form
%>
<div class="yui-b content">
    <p>${h.link_to('< Back to all blog entries', url=url('articles'))}</p>
    <h1>${_('Add new blog posting')}</h1>
    ${new_article_form(action=url('articles')) | n}
</div>
<%def name="title()">${parent.title()} - ${'Blog'} - ${c.article.title}</%def>
<%inherit file="/layout.mako" />
