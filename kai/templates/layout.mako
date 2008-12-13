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
            <h1 id="logo" class="replace">PylonsHQ<span>.</span></h1>
            ${nav(getattr(c, 'active_tab', None), getattr(c, 'active_sub', None))}
        </div>
        <div id="bd">
            % if request.environ['pylons.routes_dict']['controller'] != 'accounts':
            <div id="loginbar">
                <div class="links">
                % if session.get('logged_in'):
                    Welcome ${session['displayname']}
                    ${h.link_to('Logout', url=url('account_logout'))}
                % else:
                ${h.link_to('Login', url=url('account_login'))} or 
                ${h.link_to('Register', url=url('account_register'))}
                % endif
                </div>
            </div>
            % endif
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
</body>
</html>
<%def name="yui_class()"></%def>
<%def name="more_body()"></%def>
<%def name="title()">PylonsHQ</%def>
<%def name="styles()">
% if c.use_minified_assets:
    ${h.stylesheet_link('/css/phq-06202008.1-min.css')}
% else:
    ${h.stylesheet_link(*h.load_stylesheet_assets())}
%endif
</%def>
<%def name="javascript()">
<script type="text/javascript" src="/javascripts/jquery-1.2.6.min.js" charset="utf-8"></script>
<script type="text/javascript" src="/javascripts/jquery.blockUI.js" charset="utf-8"></script>
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
##        <li${active_sub.get('The Team', '') | n}><a href="#">The Team</a></li>
      </ul>
    </li>
    <li id="nav-2"${active_tab.get('Documentation', '') | n}>${h.link_to('Documentation', url=url('doc_home'))}
      <ul>
        <li${active_sub.get('Reference', '') | n}>${h.link_to('Reference', url=url('doc_home'))}</li>
##        <li${active_sub.get('FAQ', '') | n}><a href="#">FAQ</a></li>
        <li${active_sub.get('Modules', '') | n}>${h.link_to('Modules', url=url('doc_view', url='modules/'))}</li>
        <li${active_sub.get('Glossary', '') | n}>${h.link_to('Glossary', url=url('doc_view', url='glossary/'))}</li>
        <li${active_sub.get('Index', '') | n}><a href="#">${h.link_to('Index', url=url('doc_view', url='index/'))}</a></li>
      </ul>
    </li>
    <li id="nav-3"${active_tab.get('Community', '') | n}><a href="#">Community</a>
      <ul>
        <li${active_sub.get('Blog', '') | n}><a href="#">Blog</a></li>
        <li${active_sub.get('Wiki', '') | n}>${h.link_to('Wiki', url=url('wiki'))}</li>
##        <li${active_sub.get('Jobs', '') | n}><a href="#">Jobs</a></li>
##        <li${active_sub.get('Sites Using Pylons', '') | n}><a href="#">Sites Using Pylons</a></li>
##        <li${active_sub.get('Aggregator', '') | n}><a href="#">Aggregator</a></li>
      </ul>
    </li>
    <li id="nav-4"${active_tab.get('Tools', '') | n}><a href="#">Tools</a>
      <ul>
        <li${active_sub.get('Pastebin', '') | n}><a href="#"> Pastebin</a></li>
        <li${active_sub.get('Tracebacks', '') | n}>${h.link_to('Tracebacks', url=url('tracebacks'))}</li>
        <li${active_sub.get('Snippets', '') | n}><a href="#">${h.link_to('Snippets', url=url('snippet_home'))}</a></li>
      </ul>
    </li>
    <li id="nav-5"${active_tab.get('Code', '') | n}><a href="#">Code</a>
      <ul>
        <li${active_sub.get('Contributing', '') | n}><a href="#">Contributing</a></li>
        <li${active_sub.get('Milestones', '') | n}><a href="#">Milestones</a></li>
        <li${active_sub.get('View Tickets', '') | n}><a href="#">View Tickets</a></li>
        <li${active_sub.get('Source', '') | n}><a href="#">Source</a></li>
##        <li${active_sub.get('Releases', '') | n}><a href="#">Releases</a></li>
        <li${active_sub.get('Buildbots', '') | n}>${h.link_to('Buildbots', url=url('buildbot', action='index'))}</li>
      </ul>
    </li>
  </ul>
</div>
</%def>