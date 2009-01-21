<div class="yui-b content">
    <h1>Features</h1>
    
    <h2>Comfortable Interactive Debugger</h2>
    
    <p>Programming means making mistakes. And searching for the cause of an error
    distracts you from the task at hand and is annoying. Especially in web
    applications you usually do not have a fancy debugger at hand that allows you
    to view all variables and the piece of code where the error occurred.</p>
    
    <p>Pylons
    offers a great online debugger. If your application throws an exception you
    will get a traceback on the web page, can view local variables and can even
    enter Python statements interactively. Sometimes people even deliberately throw
    in a ``raise Exception`` statement to make the application stop at that line so
    they can investigate what is going on.</p>
    
    <p>The debugger even works with AJAX
    requests as it prints the debug URL on the console for a sub-request that you
    can just paste in your browser and debug it. And in case your application
    runs on a production server and get into an error situation it will collect
    all that information and send your an email.</p>
    
    <h2>Exploring the world: Paster shell</h2>
    
    <p>A Pylons application uses many different Python modules. The environment
    in which your application is running seems pretty opaque. Fortunately you can
    run the ``paster shell`` which is a normal Python shell (or even an *ipython*
    shell if you have it installed) but has access to all the global variables and
    utility functions that Pylons offers.</p>
    
    <p>Play with your database models, explore
    the "Webhelpers" utilities, browse through the available global variables and
    even simulate requests as if you used a browser. And if things work as you
    expect you just copy the code into your application.</p>
    
    <h2>Web server built in</h2>
    
    <p>Pylons uses *Paste* for setting up a project, upgrading it to a newer Pylons
    version and deploying the application. And it even features a built-in web
    server that you can use to develop and test your applications. You don't have to
    install an additional web server like Apache to run your application.
    Development happens directly on your workstation. And the Paste web server is
    even powerful enough that some people use in on production servers.</p>
    
    <h2>Simplifying the development cycle: --reload</h2>
    
    <p>Developing under a web framework means that your framework has to be restarted
    once you changed something. If you use the Paste web server you can toss in the
    ``--reload`` option so that Paste will monitor your files. Once you save a
    changed file it will automatically detect that and reload the framework. Your
    development cycle is essentially saving the file and reloading the page in the
    browser. It could not be simpler.</p>
    
    <h2>WSGI - ready for production use</h2>
    
    <p>Pylons does not depend on a certain web server. Other frameworks may have a web
    server built in - so you depend on its stability, security and features. Pylons
    is a WSGI framework which means that it works on any web server that speaks
    WSGI. WSGI is a protocol between web servers and web applications - similar to
    CGI. Basically any WSGI web application can run with any WSGI web server. And
    you can even use WSGI *middleware* which is code you can simply plug between the
    web server and the web application to provide features like authentication or
    logging.</p>
    
    <h2>Smooth upgrades</h2>
    
    <p>Pylons is a template for your project. It creates a number of files and
    directories where your HTML templates, database models and controller code goes
    into. You will surely change that template a lot. But what happens when a new
    version of Pylons is released? No problem. Pylons can show you the differences
    between your files and the new template and you are free to adopt any changes.
    So you are always up-to-date without starting from scratch.</p>
    
    <h2>The web developer's toolbox: Webhelpers</h2>
    
    <p>To avoid reinventing the wheel Pylons applications can use the *Webhelpers*
    package. It contains functions to deal with HTML tags and HTML forms, they convert
    numbers into human-readable forms, deal with RSS feeds and split large outputs
    (like database tables) into pages by only a few lines of Python code.</p>
    
    <h2>Beautiful URLs</h2>
    
    <p>Usually you don't have complete control over the URL in web applications. They
    look like ``/cgi-bin/myscript.pl?search=weather`` or
    ``/customers/settings.php?customerid=123``. Pylons instead uses *Routes*
    to map any URL scheme to different parts of your application. So you will
    rather end up with user-friendly and memorable URLs like ``/articles/2008``
    or ``/products/computer/keyboards``.</p>
    
    <h2>Exchangeable components</h2>
    
    <p>Pylons is open-minded. You can use it with different templating languages and
    different database toolkits. A good selection of components is already
    configured so that you can get started quickly. But it is really easy to replace
    them if they do not match your taste.</p>
    
    <h2>Separated models, views and controllers</h2>
    
    <p>In Pylons you separate the models (your database schema), the views (HTML
    templates) and the controllers (your application code). That is called *MVC*
    (model, view, controller). Using this MVC approach you can change database
    models or the HTML templates without risking to break your application code.</p>
    
</div>
<%def name="title()">${parent.title()} - ${_('Features')}</%def>
<%inherit file="/layout.mako" />
<%namespace name="widgets" file="/widgets.mako"/>
