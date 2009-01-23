<div class="yui-b content">
    <div id="searchcontrol"/>
</div>
<%def name="styles()">
<link href="http://www.google.com/uds/css/gsearch.css" type="text/css" rel="stylesheet"/>
<script src="http://www.google.com/uds/api?file=uds.js&amp;v=1.0&amp;key=ABQIAAAAgvmgA94hbkqC7kh6JzKluxQQvUAzTIjSyGWv2egO9TxsQcw_PhRfptE4k-DD1r2KrOOojaXEJjVp-Q" type="text/javascript"></script>
<script type="text/javascript">
var fixurl = {update: function (searchControl, searcher, query) {
    window.location.hash = encodeURIComponent(query).replace(/%20/g, "+");
}};

function cse() {
    // Grab the form element we use
    var sFormDiv = document.getElementById("searchcontrol");
    
    // Create a search control
    var searchControl = new GSearchControl();
    var options;
    var searcher;
    var cseId = "017012331895443894274:qqjvs4jj_ag";
    
    searcher = new GwebSearch();
    options = new GsearcherOptions();
    options.setExpandMode(GSearchControl.EXPAND_MODE_OPEN);
    searcher.setSiteRestriction(cseId, null);
    searcher.setUserDefinedLabel("Web");
    searchControl.addSearcher(searcher, options);
    
    searcher = new GwebSearch();
    options = new GsearcherOptions();
    options.setExpandMode(GSearchControl.EXPAND_MODE_OPEN);
    searcher.setSiteRestriction(cseId, "IRCLogs");
    searcher.setUserDefinedLabel("IRC Logs");
    searchControl.addSearcher(searcher, options);


    searcher = new GblogSearch();
    options = new GsearcherOptions();
    searcher.setQueryAddition("pylons python");
    searcher.setUserDefinedLabel("Blogs");
    searchControl.addSearcher(searcher, options);

    // Setup search control settings
    searchControl.setSearchStartingCallback(fixurl, fixurl.update)
    searchControl.setResultSetSize(GSearch.LARGE_RESULTSET);
    
    var drawOptions = new GdrawOptions();
    drawOptions.setDrawMode(GSearchControl.DRAW_MODE_TABBED);

    // Tell the searcher to draw itself and tell it where to attach
    searchControl.draw(sFormDiv, drawOptions);

    // Execute an inital search, use the existing anchor param if present
    var query = decodeURIComponent(location.hash.substring(1).replace(/\+/g, "%20"));
    if (query) {
        searchControl.execute(query);
    } else {
        searchControl.execute("wsgi response");
    }
}

function OnLoad() {
new cse();
}
GSearch.setOnLoadCallback(OnLoad);
</script>
<style type="text/css">

body #searchcontrol, #searchcontrol p, .gs-snippet {
  background-color: white;
  font-family: Arial, sans-serif;
  font-size: 13px;
}

h1 .tagline,
h1 a,
h1 a .tagline {
font-size : 13px;
font-weight : normal;
color : rgb(9, 122, 182);
cursor : pointer;
text-decoration : none;
}

a span.tagline:hover {
text-decoration : underline;
color : rgb(237, 92, 11);
}

a, a:link, a:visited, a:active {
    border-bottom: none;
}

.gsc-control {
    width:100%;
    max-width: 600px;
}

form .gsc-search-box {
    width: 350px;
}

table.gsc-branding {
    width: 350px;
}

table.gsc-resultsHeader, div.gsc-blogConfig {
    width: 400px;
}

/* disable twiddle and size selectors for left column */
#searchcontrol .gsc-twiddle {
  background-image : none;
}

#searchcontrol .gsc-resultsHeader .gsc-title {
  padding-left : 0px;
  font-weight : bold;
  font-size : 14px;
}

#searchcontrol .gsc-resultsHeader {
  width: 200px;
}

#searchcontrol .gsc-resultsHeader div.gsc-results-selector {
  display : none;
}

#searchcontrol .gsc-resultsRoot {
  padding-top : 6px;
}

/* long form visible urls should be on */
.gsc-webResult div.gs-visibleUrl-short {
    display: none;
}

.gsc-webResult div.gs-visibleUrl-long {
    display: block;
}

</style>
</%def>
<%inherit file="/layout.mako"/>    
