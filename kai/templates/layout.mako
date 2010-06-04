<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>${self.title()}</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    ${self.styles()}
</head>
<body>
    <div id="doc4"${self.yui_class()}>
        <div id="hd">
            <h1 id="logo"><a href="${url('home')}">Pylons</a></h1>
            ${nav(getattr(c, 'active_tab', None), getattr(c, 'active_sub', None))}
        </div>
        <div id="bd">
            <div id="loginbar">
                <div class="layoutstyle">
                    Layout: ${h.link_to('Fixed-width', id_='layout-toggle', url='#')}
                </div>
                <div class="links">
                % if session.get('logged_in'):
                    Logged in as ${session['displayname']}
                    ${h.link_to('Logout', url=url('account_logout', redir=request.path_qs))}
                % else:
                ${h.link_to('Login', url=url('account_login', redir=request.path_qs))} or 
                ${h.link_to('Register', url=url('account_register', redir=request.path_qs))}
                % endif
                </div>
            </div>
            % for message_type in ['success', 'failure']:
            <% 
                messages = getattr(h, '%s_flash' % message_type).pop_messages() 
            %>
            % if messages:
            <ul id="${message_type}-flash-messages">
            % for message in messages:
                <li>${message}</li>
            % endfor
            </ul>
            % endif
            % endfor
            ${next.body()}
            ## Load Javascripts and such at the end
            ${self.more_body()}
        </div>
        <div id="ft">
            <p>Powered by Pylons - <a href="#">Contact Administrators</a></p>
        </div>
    </div>
    ${self.javascript()}
    <script type="text/javascript">
    /*
    Inserts GA using DOM insertion of <script> tag and "script onload" method to
    initialize the pageTracker object. Prevents GA insertion from blocking I/O!

    As suggested in Steve Souder's talk. See:
    http://google-code-updates.blogspot.com/2009/03/steve-souders-lifes-too-short-write.html
    */

    /* acct is GA account number, i.e. "UA-5555555-1" */
    function gaSSDSLoad (acct) {
      var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www."),
          pageTracker,
          s;
      s = document.createElement('script');
      s.src = gaJsHost + 'google-analytics.com/ga.js';
      s.type = 'text/javascript';
      s.onloadDone = false;
      function init () {
        pageTracker = _gat._getTracker(acct);
        pageTracker._trackPageview();
      }
      s.onload = function () {
        s.onloadDone = true;
        init();
      };
      s.onreadystatechange = function() {
        if (('loaded' === s.readyState || 'complete' === s.readyState) && !s.onloadDone) {
          s.onloadDone = true;
          init();
        }
      };
      document.getElementsByTagName('head')[0].appendChild(s);
    }
    /* and run it */
    gaSSDSLoad("UA-341777-2");
    </script>
</body>
</html>
<%def name="yui_class()"></%def>
<%def name="more_body()"></%def>
<%def name="title()">PylonsHQ</%def>
<%def name="styles()">
% if c.use_minified_assets:
    ${h.stylesheet_link('/css/%s' % config['phq.minified_css'])}
% else:
    ${h.stylesheet_link(*h.load_stylesheet_assets())}
%endif
</%def>
<%def name="javascript()">
<script src="http://cdn.jquerytools.org/1.2.2/full/jquery.tools.min.js"></script>
<script type="text/javascript" src="/javascripts/jquery_all.js" charset="utf-8"></script>
<script type="text/javascript" src="/javascripts/behavior.js" charset="utf-8"></script>
</%def>
<%def name="nav(tab, sub)">
<div id="nav">\
<%
    active_tab = {}
    active_tab[tab or 'Home'] = ' class="selected"'
    active_sub = {}
    active_sub[sub or 'Overview'] = ' class="selected"'
%>\
  <ul class="clearfix">
    <li id="nav-1"${active_tab.get('Home', '') | n}>${h.link_to('Home', url=url('home'))}
      <ul>
        <li${active_sub.get('Overview', '') | n}>${h.link_to('Overview', url=url('home'))}</li>
        <li${active_sub.get('Features', '') | n}>${h.link_to('Features', url=url('features'))}</li>
        <li${active_sub.get('History', '') | n}>${h.link_to('History', url=url('history'))}</li>
        <li${active_sub.get('Search', '') | n}>${h.link_to('Search', url=url('search'))}</li>
##        <li${active_sub.get('The Team', '') | n}><a href="#">The Team</a></li>
      </ul>
    </li>
    <li id="nav-2"${active_tab.get('Documentation', '') | n}>${h.link_to('Documentation', url=url('doc_home', version=session.get('doc_version', app_globals.doc_version)))}
      <ul>
        <li${active_sub.get('Reference', '') | n}>${h.link_to('Reference', url=url('doc_home', version=session.get('doc_version', app_globals.doc_version)))}</li>
##        <li${active_sub.get('FAQ', '') | n}><a href="#">FAQ</a></li>
        <li${active_sub.get('Modules', '') | n}>${h.link_to('Modules', url=url('doc_view', url='modules/', version=session.get('doc_version', app_globals.doc_version)))}</li>
        <li${active_sub.get('Glossary', '') | n}>${h.link_to('Glossary', url=url('doc_view', url='glossary/', version=session.get('doc_version', app_globals.doc_version)))}</li>
        <li${active_sub.get('Index', '') | n}><a href="#">${h.link_to('Index', url=url('doc_view', url='index/', version=session.get('doc_version', app_globals.doc_version)))}</a></li>
      </ul>
    </li>
    <li id="nav-3"${active_tab.get('Community', '') | n}>${h.link_to('Community', url=url('community'))}
      <ul>
        <li${active_sub.get('Blog', '') | n}>${h.link_to('Blog', url=url('articles'))}</li>
        <li${active_sub.get('Wiki', '') | n}>${h.link_to('Wiki', url=url('wiki'))}</li>
##        <li${active_sub.get('Jobs', '') | n}><a href="#">Jobs</a></li>
##        <li${active_sub.get('Sites Using Pylons', '') | n}><a href="#">Sites Using Pylons</a></li>
##        <li${active_sub.get('Aggregator', '') | n}><a href="#">Aggregator</a></li>
      </ul>
    </li>
    <li id="nav-4"${active_tab.get('Tools', '') | n}><a href="${url('pasties')}">Tools</a>
      <ul>
        <li${active_sub.get('Pastebin', '') | n}>${h.link_to('Pastebin', url=url('pasties'))}</li>
        <li${active_sub.get('Tracebacks', '') | n}>${h.link_to('Tracebacks', url=url('tracebacks'))}</li>
        <li${active_sub.get('Snippets', '') | n}><a href="#">${h.link_to('Snippets', url=url('snippets'))}</a></li>
      </ul>
    </li>
    <li id="nav-5"${active_tab.get('Code', '') | n}>${h.link_to('Code', url=url('trac_link', url='roadmap'))}
      <ul>
        <li${active_sub.get('Contributing', '') | n}>${h.link_to('Contributing')}</li>
        <li${active_sub.get('Milestones', '') | n}>${h.link_to('Milestones', url=url('trac_link', url='roadmap'))}</li>
        <li${active_sub.get('View Tickets', '') | n}>${h.link_to('View Tickets', url=url('trac_link', url='report'))}</li>
        <li${active_sub.get('Source', '') | n}>${h.link_to('Source', url=url('trac_link', url='browser'))}</li>
##        <li${active_sub.get('Releases', '') | n}><a href="#">Releases</a></li>
##        <li${active_sub.get('Buildbots', '') | n}>${h.link_to('Buildbots', url=url('buildbot', action='index'))}</li>
      </ul>
    </li>
  </ul>
</div>
</%def>
