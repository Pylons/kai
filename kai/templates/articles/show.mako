<div class="yui-b content">
    <p>${h.link_to('< Back to all blog entries', url=url('articles'))}</p>
    ${article.display_article(c.article)}
</div>
<%namespace name="article" file="index.mako"/>
<%def name="title()">${parent.title()} - Blog - ${c.article.title}</%def>
<%inherit file="/layout.mako" />
