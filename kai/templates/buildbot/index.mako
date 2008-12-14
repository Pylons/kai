<div class="yui-b content">
    <h1>Buildbot Status</h1>
    <p>Pylons source code is <strong>automatically built and tested</strong> via
        <a href="http://buildbot.net/trac">Buildbot</a> to ensure consistent
        release quality and track bugs that may occur during development (also
        known as <strong><a href="http://en.wikipedia.org/wiki/Continuous_Integration">
            Continuous integration</a></strong>). The
        latest builds are posted here automatically as they're
        completed. For those tracking the latest development tip, this can serve
        as a useful reference when decided whether to update.</p>
    
    <p>In <a href="http://www.selenic.com/mercurial/">Mercurial</a>, the revision
        control system (RCS) used by Pylons, the latest revision is called the
        tip.</p>
    
    <h2>Latest Release (${app_globals.current_version})</h2>
    ${build_table(c.releases)}
    <div class="loadmore viewtoggle release"><a href="#">Older release builds</a></div>
    <div class="older release" style="display: none;">
        ${build_table(c.releases, start=1, limit=None, include_header=None)}
    </div>
    
    <div class="clearfix">&nbsp;</div>
    
    <h2>Development Tip</h2>
    ${build_table(c.dev)}
    <div class="loadmore viewtoggle dev"><a href="#">Older tip builds</a></div>
    <div class="older dev" style="display: none;">
        ${build_table(c.dev, start=1, limit=None, include_header=None)}
    </div>
    
    <br /><br /><br />
    <div id="buildinfo" style="display:none; cursor: default">
        <h1>Loading...</h1>
    </div>
</div>
<%def name="build_table(builds, start=0, limit=1, include_header=True)">
<table class="buildbot">\
    % if include_header:
    <thead>
        <tr>
            <th colspan="${len(builds)}">Build Name</th>
        </tr>
        <tr>
            % for build in sorted(builds.keys()):
            <th>${build}
            % endfor
    </thead>
    % endif
    <tbody>
        <%
            here = start
            limit = limit
            stop = 100
            for build in sorted(builds.keys()):
                newmin = len(builds[build]) - 1
                if newmin < stop:
                    stop = newmin
        %>
        % while True:
        <tr class="run">
            % for build in sorted(builds.keys()):
            <% 
                time = builds[build][here]['end']
            %>
            <td>${format.datetime(time, "medium")}</td>
            % endfor
        </tr>
        <tr>
            % for build in sorted(builds.keys()):
            <% item = builds[build][here] %>
            <td class="result">
            <div class="details"><a href="#" class="${'%s__%s' % (item['name'], item['version'])}">&nbsp;</a></div>
            % if not item['reasons']:
            <span class="${item['results']}">${item['results']}</span>
            % endif
            % for reason in item['reasons']:
                <span class="failure">${reason[0]}</span><br />
            % endfor
            </td>
            % endfor
        </tr>
        <%
            here += 1
            if limit and here == limit:
                break
            elif here > stop:
                break
        %>
        % endwhile
    </tbody>
</table>
</%def>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />