<%def name="styles()">
${parent.styles()}
${h.stylesheet_link('/css/sphinx.css')}
<link rel="stylesheet" href="/css/jquery.rating.css" type="text/css" media="screen" title="no title" charset="utf-8">
<style type="text/css" media="screen">
#report_box {
	height: 150px;
	width: 450px;
	border: thin solid #545454;
	position: absolute;
	background-color: #dedede;
	padding: 10px;
	margin-left: 23%;
	margin-right: 33%;
	display: none;
}

textarea {
    width: 98%;
    height: 100px;
    font-size: 12px;
    margin-bottom: 5px;
}

#rating_area {
    float: right;
    text-align: right;
    margin-top: -35px;
}

.rating{
	width:80px;
	height:16px;
	padding:0;
	list-style:none;
	position:relative;
	background: url(/css/images/star-matrix.gif) no-repeat 0 0;
	display: block;
	clear: none;
	text-align: center;
}

.rating_text {
    margin-right: 15px;
    font-size: 12px;
    color: #ababab;
}
/* add these classes to the ul to effect the change to the correct number of stars */
.nostar {background-position:0 0;
}
.onestar {background-position:0 -16px}
.twostar {background-position:0 -32px}
.threestar {background-position:0 -48px}
.fourstar {background-position:0 -64px}
.fivestar {background-position:0 -80px}

ul.rating li {
	cursor: pointer;
 /*ie5 mac doesn't like it if the list is floated\*/
	float:left;
	/* end hide*/
	text-indent:-999em;
	list-style: none;
}
ul.rating li a {
	position:absolute;
	left:0;
	top:0;
	width:16px;
	height:16px;
	text-decoration:none;
	z-index: 200;
}
ul.rating li.one a {left:0}
ul.rating li.two a {left:16px;}
ul.rating li.three a {left:32px;}
ul.rating li.four a {left:48px;}
ul.rating li.five a {left:64px;}
ul.rating li a:hover {
	z-index:2;
	width:80px;
	height:16px;
	overflow:hidden;
	left:0;	
	background: url(/css/images/star-matrix.gif) no-repeat 0 0
}
ul.rating li.one a:hover {background-position:0 -96px;}
ul.rating li.two a:hover {background-position:0 -112px;}
ul.rating li.three a:hover {background-position:0 -128px}
ul.rating li.four a:hover {background-position:0 -144px}
ul.rating li.five a:hover {background-position:0 -160px}
/* end rating code */

</style>

</%def> 

<%def name="javascript()">
${parent.javascript()}
<script src="/javascripts/jquery.rating.js" type="text/javascript" charset="utf-8"></script>
<script type="text/javascript" charset="utf-8">
    $('#report').click(function() {
        $("#report_box").toggle();
    })
    
    /* handle the ratings */
   $('ul.rating').click( function(e){ 
       $el=$(e.target);
       //check what $el is here and do stuff
       var ulid = $el.parents('ul:first').attr('id')
       var type = ulid.substr(0,1)
       var id = ulid.substr(2)
       var rating = $el.parent().attr('class')
       
       $.post('/rating', {'id': id, 'type': type, 'rating': rating}, function(data) {
           var class = $el.parents('ul:first').attr('class')
           $el.parents('ul:first').removeClass(class)
           $el.parents('ul:first').addClass('rating ' + data)
       });
       
   })
</script>
</%def>

<div class="yui-b content">
	<div class="relnav" id="relnav">
		<a href="${url('snippet_add')}">Add Snippet</a> | <a href="javascript:void(0);" id="report">Report Snippet</a> | <a href="#">View By Rating</a> | <a href="#">View By Author</a> | <a href="#">Search</a>
	</div>
	<div id="report_box">
	    <form method="POST" action="${url('snippet_report')}">
	    <label for="reason">Reason:</label><br />
	    <textarea name="reason" id="reason" value="reason"></textarea>
	    <br />
	    <input type="submit"  value="Report Snippet" />
	    </form>
	</div>
    <h1>${c.snippet.title}</h1>
    <div id="rating_area">
        <span class="rating_text">Rating:</span> 
        <ul class="rating nostar">
        <li class="one"><a href="#" title="1 Star">1</a></li>
        <li class="two"><a href="#" title="2 Stars">2</a></li>
        <li class="three"><a href="#" title="3 Stars">3</a></li>

        <li class="four"><a href="#" title="4 Stars">4</a></li>
        <li class="five"><a href="#" title="5 Stars">5</a></li>
        </ul>
    </div>

	
    <p>${c.snippet.description|n}</p>
	<p>${c.snippet_content|n}</p>
	<p>
	<h5>Author: <a href="${url(controller='snippets', action='by_author', id=c.snippet.human_id)}">${c.snippet.username}</a></h5>
	<h5>Tags: 
	% for tag in c.snippet.tags:
		<a href="${url(controller='snippets', action='by_tag', tag=tag.strip())}">${tag}</a>
	% endfor
	</h5>
	</p>
</div>


<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />