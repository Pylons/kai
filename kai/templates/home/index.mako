<div id="yui-main">
    <div id="intro">
      <h2>Pylons is a lightweight web framework <br />
        emphasizing flexibility and rapid development.</h2>
      <div id="download"> <a href="#">Download Latest </a> Version: ${app_globals.current_version}</div>
    </div>
</div> 
  <div class="yui-b">
    <div class="yui-gc">
      <div class="yui-u first">
        <h3>Why use Pylons?</h3>
        <p>Pylons combines the very best ideas from the worlds of Ruby, Python and Perl, providing a structured but extremely flexible Python web framework. It's also one of the first projects to leverage the emerging WSGI standard, which allows extensive re-use and flexibility — but only if you need it. Out of the box, Pylons aims to make web development fast, flexible and easy. <a href="#">Find out more</a>, <a href="#">Install the latest version</a> or <a href="#">Start learning Pylons</a>. </p>
        <h3>Plays Well With Others </h3>
        <p>Pylons is built on <a href="#">Paste</a> and allows and encourages use of your favorite Python components and libraries: </p>
        <ol>
          <li>Models: <a href="#">SQLAlchemy</a>, <a href="#">SQLObject</a>, plain old DB-API </li>
          <li>Templating: Mako, Genshi, Jinja, Kid, Cheetah, or whatever you like - using Buffet </li>
          <li>AJAX: Rails-style WebHelpers based on Prototype, or Mochikit, jQuery, Dojo, Ext &amp; more </li>
          <li>Request Dispatching: Routes by default, or plug in your favorite</li>
        </ol>
        <p><strong>Not sure which one to choose?</strong> No problem! Pylons recommends and documents
            using a powerful templating solution (Mako) and database ORM (SQLAlchemy) to help you get started.</p>
        <h3>Latest Tutorials </h3>
        <ul>
          <li><a href="#">Pylons Screencasts </a></li>
          <li><a href="#">How to write a basic blog with Pylons </a></li>
          <li><a href="#">Getting started with AJAX </a></li>
          <li><a href="#">Porting Rails Flickr Example </a></li>
          <li><a href="#">Production Deployment Using Apache, FastCGI and mod_rewrite </a></li>
        </ul>
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
<%inherit file="/layout.mako" />