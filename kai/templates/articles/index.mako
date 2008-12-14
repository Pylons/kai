<div class="yui-b content">
    <h1>${_('Recent Blog Postings')}</h1>
    % for article in c.articles:
    ${display_article(article)}
    % endfor
</div>
<%def name="display_article(article)">
<div class="atomentry" id="article-${article.slug}">
    <h2 class="title">${h.link_to(article.title, url=url('article_archives', article=article))}</h2>
    <%
        author = '<cite>%s</cite>' % article.author
        date = '<span class="date">%s</span>' % format.date(article.published, "long")
        post_dict = dict(author=author, date=date)
    %>
    <p class="author">${_('Posted by %(author)s on %(date)s' % post_dict) | n}</p>
    <div class="articlecontent">
        ${h.textilize(article.body)}
    </div>
</div>
</%def>
<%def name="title()">${parent.title()} - Blog</%def>
<%inherit file="/layout.mako" />
