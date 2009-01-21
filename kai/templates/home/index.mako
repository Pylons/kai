<div id="yui-main">
    <div id="intro">
      <h2>${_("""Pylons is a lightweight web framework <br />
        emphasizing flexibility and rapid development.""") | n}</h2>
      <div id="download"> <a href="${url('doc_view', url='gettingstarted/', anchor='installing')}">${_('Download Latest')} </a> ${_('Version: %s' % app_globals.current_version)}</div>
    </div>
</div> 
  <div class="yui-b">
    <div class="yui-gc">
      <div class="yui-u first">
        <h3>${_('Why use Pylons?')}</h3>
        <p>Pylons combines the very best ideas from the worlds of Ruby, Python and Perl, providing a structured but
            extremely flexible Python web framework. It's also one of the first projects to leverage the emerging
            WSGI standard, which allows extensive re-use and flexibility — but only if you need it. Out of the box,
            Pylons aims to make web development fast, flexible and easy. 
            ${h.link_to('Find out more', url=url('doc_home'))}, 
            ${h.link_to('install the latest version', url=url('doc_view', url='gettingstarted/', anchor='installing'))}, 
            or <b>${h.link_to('read the new Pylons book', url=url('pylons_book'))}</b>. </p>

        <h3>${_('Plays Well With Others')}</h3>
        <p>Pylons is built on <a href="#">Paste</a> and allows and encourages use of your favorite Python components and libraries: </p>
        <ol>
          <li>Models: ${h.link_to('SQLAlchemy', url=url('sqlalchemy'))}, ${h.link_to('SQLObject', url=url('sqlobject'))}, ${h.link_to('CouchDB', url=url('python-couchdb'))}, or none at all</li>
          <li>Templating: ${h.link_to('Mako', url=url('mako'))}, ${h.link_to('Genshi', url=url('genshi'))}, ${h.link_to('Jinja2', url=url('jinja2'))}, or whatever you like</li>
          <li>Helpers: WebHelpers for small HTML snippets, ${h.link_to('FormAlchemy', url=url('formalchemy'))} generates entire forms</li>
          <li>Request Dispatching: Routes by default, or plug in your favorite</li>
        </ol>
        <p><strong>Not sure which one to choose?</strong> No problem! The Pylons documentation recommends a powerful templating engine (Mako) and database ORM (SQLAlchemy) to help you get started.</p>
        <h3>Latest Tutorials </h3>
        <ul>
          <li><a href="http://www.pylonscasts.com/">Pylons screencasts </a></li>
          <li><a href="http://wiki.pylonshq.com/display/pylonscookbook/Production+Deployment+Using+Apache,+FastCGI+and+mod_rewrite">Production deployment using Apache, FastCGI and mod_rewrite </a></li>
        </ul>
      </div>
      <div class="yui-u" id="sidebar">
##        <div id="search">
##          <form action="">
##            <input type="text" name="search" id="search-input" />
##            <button type="submit">${_('Search')}</button>
##          </form>
##        </div>
        <div id="news" class="side-section">
          <h3>${_('Latest News')}</h3>
          <ul>
              % for article in c.articles:
                <li><strong>${h.link_to(article.title, url=url('article_archives', article=article))}</strong><br />
                    ${format.date(article.published)}</li>
              % endfor
              <li><strong>${h.link_to('More', url=url('articles'))}</strong></li>
          </ul>
        </div>
        <div id="usefull" class="side-section">
          <h3>${_('Useful Resources')}</h3>
          <p>You might be interested to see the production 
              <a href="http://wiki.pylonshq.com/display/pylonscommunity/Sites+Using+Pylons">sites already using Pylons</a>. If you are after specific information not found in the
               <a href="${url('doc_home')}">documentation</a>, have a look at the <a href="${url('wiki')}">wiki</a>.  The ${h.link_to('wiki', url=url('wiki'))} is a useful
                resource for Pylons programming. You might also consider adding an article of your own.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="clearfix">&nbsp;</div>
  <div class="yui-b" id="bottom-content">
    <div class="yui-gc">
      <div class="yui-g first">
        <div class="yui-u first">
          <h4>${_('Recent Snippets')}</h4>
          <ul>
            % for snippet in c.snippets:
            <li>${h.link_to(snippet.title, url=url('snippet', id=snippet.slug))}<br />
                ${h.truncate(snippet.description, length=90, whole_word=True)}</li>
            % endfor
          </ul>
        </div>
        <div class="yui-u">
          <h4>${_('Recent Pastes')}</h4>
          <ul>
              % for paste in c.pastes:
              <li>${h.link_to(paste.title, url=url('paste', id=paste.old_id or paste.id))}<br />
                  ${widgets.format_timestamp(paste.created)}<br />
                  % if len(paste.tags) > 0:
                  <span class="tagheader">Tags: </span>\
                      % for tag in paste.tags:
                          % if tag:
                          ${h.link_to(tag, url=url('pasties_tag', tag=tag))} 
                          % endif
                      % endfor
                  % endif
              </li>
              % endfor
          </ul>
        </div>
      </div>
      <div class="yui-u" id="bottom-content-sidebar">
        <div id="join" class="side-section">
          <h3><a href="http://groups.google.com/group/pylons-discuss">${_('Join the discussion')}</a></h3>
          <form action="">
            <p>
              <label for="join-nam">Name:</label>
              <input type="text" name="name" id="join-name" class="input" />
              
            </p>
            <p>
              <label for="join-email">Email:</label>
              <input type="text" name="eamil" id="join-email" class="input" />
              
            </p>
            <button type="submit">${_('Join Mailing List')}</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<%def name="title()">${parent.title()} - ${_('Home')}</%def>
<%def name="yui_class()"> class="home"</%def>
<%inherit file="/layout.mako" />
<%namespace name="widgets" file="/widgets.mako"/>
<%def name="styles()">
${h.auto_discovery_link(url('formatted_articles', format='atom', qualified=True), feed_type='atom', title='PylonsHQ News Feed')}
${h.auto_discovery_link(url('formatted_snippets', format='atom', qualified=True), feed_type='atom', title='PylonsHQ Snippet Feed')}
${h.auto_discovery_link(url('formatted_pasties', format='atom', qualified=True), feed_type='atom', title='PylonsHQ Pasties Feed')}
${parent.styles()}
</%def>