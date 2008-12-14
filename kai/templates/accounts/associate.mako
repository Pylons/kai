<%!
    from kai.model.forms import login_form
%>
<div class="yui-b content">
    <h1>OpenID Association</h1>
    
    <p>The OpenID URL you used (<b>${c.openid}</b>) was not found
        in our database. If you would like to associate this OpenID URL with
        an existing account so that you can use this OpenID URL to login with
        in the future, proceed below.</p>
    
    <p>If you would like to register with PylonsHQ instead,
        ${h.link_to('continue on to the registration page', url=url('openid_register'))}.
    
    ${login_form(action=url('openid_associate')) | n}    
</div>
<%def name="title()">${parent.title()} - Associate OpenID Account</%def>
<%inherit file="../layout.mako" />