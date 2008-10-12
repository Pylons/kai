  <div class="yui-b">
    <div class="yui-gc">
      <div class="yui-u first">
        <h3>Add a Snippet</h3>
		<p>Please only upload completed code.</p>
		<form action=""
			<h5>Title:</h5>
			<input type="text" name="title" id="input" /><br />
			<br />
			<h5>Description</h5>
			<textarea name="description" style="width: 40em; height: 5em">
			</textarea><br />
			<br />
			<h5>Snippet</h5>
			<textarea name="snippet" style="width: 40em; height: 20em">
			</textarea><br />
			<br />
			<input type="submit" value="Add Snippet" />
		</form>

      </div>
      <div class="yui-u" id="sidebar">
        <div id="search">
          <form action="">
            <input type="text" name="search" id="search-input" />
            <button type="submit">Search</button>
          </form>
        </div>
        <div id="news" class="side-section">
          <h3>Latest News</h3>
          <ul>
            <li><strong><a href="#">Pylons 0.9.6.1 Released</a></strong><br />
              Thu, 27 Sep 2007 </li>
            <li><strong><a href="#">Pylons 0.9.6.1 Released</a></strong><br />
              Thu, 27 Sep 2007 </li>
            <li><strong><a href="#">Pylons 0.9.6.1 Released</a></strong><br />
              Thu, 27 Sep 2007 </li>
            <li><strong><a href="#">More</a></strong></li>
          </ul>
        </div>
        <div id="usefull" class="side-section">
          <h3> Useful Resources</h3>
          <p>You might be <a href="#">interested to see</a> the production sites already using Pylons. If you are after specific information not found in the <a href="#">documentation</a> you should have a look at the wiki which is fast becoming a very useful resource for <a href="#"> Pylons programming</a>. You might also consider adding an article of your own.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="clearfix">&nbsp;</div>
  <div class="yui-b" id="bottom-content">
    <div class="yui-gc">
      <div class="yui-g first">
        <div class="yui-u first">
          <h4>Recent Blog Entries</h4>
          <ul>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite</li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
          </ul>
        </div>
        <div class="yui-u">
          <h4>Recent Pastebin Snippets</h4>
          <ul>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite</li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
            <li><a href="#">Lorem ipsum dolor sit amet, consectetur </a><br />
              Production Deployment Using Apache, FastCGI and mod_rewrite </li>
          </ul>
        </div>
      </div>
      <div class="yui-u" id="bottom-content-sidebar">
        <div id="join" class="side-section">
          <h3>Join the discussion</h3>
          <form action="">
            <p>
              <label for="join-nam">Name:</label>
              <input type="text" name="name" id="join-name" class="input" />
              
            </p>
            <p>
              <label for="join-email">Email:</label>
              <input type="text" name="eamil" id="join-email" class="input" />
              
            </p>
            <button type="submit">Join Mailing List</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%def name="yui_class()"> class="home"</%def>
<%inherit file="layout.mako" />