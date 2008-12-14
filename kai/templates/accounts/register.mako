<%!
    from kai.model.forms import registration_form, openid_login_form, openid_registration_form
%>
<div class="yui-b content">
    % if c.openid:
    <h1>Finish Registration</h1>
    
    <p>Using OpenID: ${c.openid}</p>
    
    ${openid_registration_form(c.defaults, action=url('openid_register')) | n}
    
    % else:
    <h1>Register for an Account</h1>
    
    <p>Create an account for the PylonsHQ site. This account will let you:
        <ul>
            <li>Post Snippets, Jobs, and Sites</li>
            <li>Comment on Tracebacks, Snippets, and Pastes'</li>
        </ul>
    </p>
    
    <p>These will be used to identify you as you contribute on the PylonsHQ site. Notifications
        from the system will be sent to this email address, as well as lost password requests.</p>
    
    <p><b>Note: </b>A valid e-mail address is required to activate your
        account.</p>
    
    ${registration_form(action=url('account_register')) | n}
    
    <div id="openid_reg">
        <h3>Register with OpenID</h3>
        <p>To speed up registration, using OpenID will automatically fill-in details
            that from the OpenID provider.</p>
        
        ${openid_login_form(action=url('openid_create')) | n}
    </div>
    % endif
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />