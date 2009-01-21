<div class="yui-b content">
    <h1>${_('Recent Blog Postings')}\
% if c.user and c.user.in_group('admin'):
 <span class="subtle">(${h.link_to('Add Posting', url=url('new_article'))})</span>\
% endif
</h1>
    <%
    if c.articles:
        results = list(c.articles)
    if c.reverse:
        results.reverse()
    %>
    
    ${widgets.pager(c.start, results, c.articles.total_rows, 'published')}
    % for article in results[:10]:
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
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="title()">${parent.title()} - ${_('Blog')}</%def>
<%inherit file="/layout.mako" />
<%def name="styles()">
${h.auto_discovery_link(url.current(format='atom', qualified=True), feed_type='atom', title='News Feed')}
${parent.styles()}
</%def>