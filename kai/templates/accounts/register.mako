<%!
    from kai.model.forms import registration_form, openid_login_form, openid_registration_form
%>
<div class="yui-b content">
    % if c.openid:
    <h1>${_('Finish Registration')}</h1>
    
    <p>${_('Using OpenID: %s' % c.openid)}</p>
    
    ${openid_registration_form.display(c.defaults, action=url('openid_register')) | n}
    
    % else:
    <h1>${_('Register for an Account')}</h1>
    
    <p>${_('Create an account for the PylonsHQ site. This account will let you:')}
        <ul>
            <li>${_('Post Snippets, Jobs, and Sites')}</li>
            <li>${_("Comment on Tracebacks, Snippets, and Pastes'")}</li>
        </ul>
    </p>
    
    <p>${_("""These will be used to identify you as you contribute on the PylonsHQ site. Notifications
        from the system will be sent to this email address, as well as lost password requests""")}.</p>
    
    <p>${_("""<b>Note: </b>A valid e-mail address is required to activate your
        account.""") |n}</p>
    
    ${registration_form.display(action=url('account_register')) | n}
    
    <div id="openid_reg">
        <h3>${_('Register with OpenID')}</h3>
        <p>${_("""To speed up registration, using OpenID will automatically fill-in details
            that from the OpenID provider.""")}</p>
        
        ${openid_login_form.display(action=url('openid_create')) | n}
    </div>
    % endif
</div>
<%def name="title()">${parent.title()} - ${_('Registration')}</%def>
<%inherit file="../layout.mako" />