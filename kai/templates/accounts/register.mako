<div class="yui-b content">
    <h1>Register for an Account</h1>
    
    <p>Create an account for the PylonsHQ site. This account will let you:
        <ul>
            <li>Post Snippets, Jobs, and Sites</li>
            <li>Comment on Tracebacks, Snippets, and Pastes'</li>
        </ul>
    </p>
    
    <div id="openid_reg">
        <h3>Register with OpenID</h3>
        <p>To speed up registration, using OpenID will automatically fill-in details
            that from the OpenID provider.</p>
        <form action="${url('account_oid_reg')}" method="POST">
            <input type="text" name="openid_uri" />
            <input type="submit" value="Register with OpenID" />
        </form>
    </div>
    
    <h2>Personal Details</h2>
    
    <p>These will be used to identify you as you contribute on the PylonsHQ site. Notifications
        from the system will be sent to this email address, as well as lost password requests.</p>
    
    
    <form action="${url('account_register')}" method="POST">
        ${h.auth_token_hidden_field()}
        <label for="displayname">Display name<br /> (this will be displayed to others, and should be your full name):</label>
        <input type="text" name="displayname" /><br />
        
        <label for="email">Email address:</label>
        <input type="text" name="email" /><br />
    
        <label for="email2">Confirm Email address:</label>
        <input type="text" name="email2" /><br />
        
        <label for="password">Password:</label>
        <input type="password" name="password" /><br />
        
        <label for="password2">Confirm Password</label>
        <input type="password" name="password2" /><br />
        
        <input type="submit" value="Register" />
    </form>
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />