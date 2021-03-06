<%!
    from kai.model.forms import forgot_password_form
%>
<div class="yui-b content">
    <h1>${_('Password Reset Request')}</h1>
    <p>${_('Enter your e-mail address to request a password reset.')}</p>
    ${forgot_password_form.display(action=url('forgot_password')) | n}
</div>
<%def name="title()">${parent.title()} - ${_('Password Reset Request')}</%def>
<%inherit file="../layout.mako" />