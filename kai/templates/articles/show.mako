<div class="yui-b content">
    <p>${h.link_to('< Back to all blog entries', url=url('articles'))}</p>
    ${article.display_article(c.article)}
    ${widgets.show_comments(c.article.id, poster_id=c.article.human_id)}
</div>
<%namespace name="article" file="index.mako"/>
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('Blog')} - ${c.article.title}</%def>
<%inherit file="/layout.mako" />
