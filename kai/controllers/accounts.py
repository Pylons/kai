from datetime import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest, secure, jsonify
from tw.mods.pylonshf import validate

from kai.lib.base import BaseController, render
from kai.lib.helpers import failure_flash, success_flash
from kai.lib.mail import EmailMessage
from kai.model import Human, forms

log = logging.getLogger(__name__)

class AccountsController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True

    @rest.dispatch_on(POST='_forgot_password')
    def forgot_password(self):
        return render('/accounts/forgot_password.mako')
    
    def verify_email(self, token):
        users = list(Human.by_email_token(self.db)[token])
        if users:
            user = users[0]
            
            # If there's a email token issue (change email address), verify
            # its still valid
            if user.email_token_issue:
                diff = datetime.utcnow() - user.email_token_issue
                if diff.days > 1 or diff.seconds > 3600:
                    failure_flash('This e-mail verification token has expired.')
                    redirect_to('home')
            
            # Valid e-mail token, remove it and log the user in
            user.email_token = None
            user.process_login()
            success_flash('Your email has been verified, and you have been'
                          ' logged into PylonsHQ')
            redirect_to('home')
        else:
            # No valid e-mail token
            failure_flash('Invalid e-mail token')
            redirect_to('home')
    
    @validate(form=forms.forgot_password_form, error_handler='forgot_password')
    @secure.authenticate_form
    def _forgot_password(self):
        user = list(Human.by_email(self.db)[self.form_result['email_address']])[0]
        user.password_token = user.generate_token()
        c.password_token = user.password_token
        user.password_token_issue = datetime.utcnow()
        user.store(self.db)
        message = EmailMessage(subject="PylonsHQ - Lost Password", 
                               body=render('/email/lost_password.mako'),
                               from_email="PylonsHQ <pylons@pylonshq.com>",
                               to=[self.form_result['email_address']])
        message.send(fail_silently=True)
        success_flash('An e-mail has been sent to your account to verify the password reset request.')
        redirect_to('account_login')
    
    @rest.dispatch_on(POST='_change_password')
    def change_password(self, token):
        users = list(Human.by_password_token(self.db)[token])
        if not users:
            failure_flash('That password token is no longer valid.')
            redirect_to('account_login')
        
        user = users[0]
        diff = datetime.utcnow() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        return render('/accounts/change_password.mako')
    
    @validate(form=forms.change_password_form, error_handler='change_password')
    @secure.authenticate_form
    def _change_password(self, token):
        users = list(Human.by_password_token(self.db)[token]) or abort(401)
        user = users[0]
        diff = datetime.utcnow() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        user.password_token = user.password_token_issue = None
        user.password = user.hash_password(self.form_result['password'])
        user.store(self.db)
        success_flash('Your password has been reset successfully')
        redirect_to('account_login')

    def logout(self):
        c.user.session_id = None
        c.user.store(self.db)
        session.clear()
        session.expire()
        session.save()
        success_flash('You have logged out of your session')
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_login')
    def login(self):
        return render('/accounts/login.mako')
    
    @validate(form=forms.login_form, error_handler='login')
    @secure.authenticate_form
    def _process_login(self):
        user = self.form_result['user']
        user.process_login()
        success_flash('You have logged into PylonsHQ')
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_openid_associate')
    def openid_associate(self):
        openid_url = session.get('openid_identity')
        if not openid_url:
            redirect_to('account_register')
        c.openid = openid_url
        return render('/accounts/associate.mako')
    
    @validate(form=forms.login_form, error_handler='login')
    def _process_openid_associate(self):
        openid_url = session.get('openid_identity')
        user = self.form_result['user']
        if user.openids:
            user.openids.append(openid_url)
        else:
            user.openids = [openid_url]
        user.process_login()
        success_flash('You have associated your OpenID to your account, and signed in')
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_openid_registration')
    def openid_register(self):
        openid_url = session.get('openid_identity')
        if not openid_url:
            redirect_to('account_register')
        c.openid = session.get('openid_identity')
        c.defaults = {}
        return render('/accounts/register.mako')
    
    @validate(form=forms.openid_registration_form, error_handler='openid_register')
    def _process_openid_registration(self):
        new_user = Human(displayname=self.form_result['displayname'],
                         timezone = self.form_result['timezone'],
                         email=self.form_result['email_address'])
        new_user.openids = [session['openid_identity']]
        return self._finish_registration(new_user)
    
    @rest.dispatch_on(POST='_process_registration')
    def register(self):
        return render('/accounts/register.mako')

    @validate(form=forms.registration_form, error_handler='register')
    @secure.authenticate_form
    def _process_registration(self):
        new_user = Human(displayname=self.form_result['displayname'],
                         timezone = self.form_result['timezone'],
                         email=self.form_result['email_address'])
        new_user.password = Human.hash_password(self.form_result['password'])
        return self._finish_registration(new_user)
    
    def _finish_registration(self, user):
        user.email_token = c.eail_token = user.generate_token()
        user.email_token_issue = datetime.utcnow()
        user.store(self.db)
        
        # Send out the welcome email with the reg token
        message = EmailMessage(subject="PylonsHQ - Registration Confirmation",
                               body=render('/email/register.mako'),
                               from_email="PylonsHQ <pylons@pylonshq.com>",
                               to=[self.form_result['email_address']])
        message.send(fail_silently=True)
        
        success_flash("User account '%s' created successfully. An e-mail has"
                      " been sent to activate your account." % user.displayname)
        redirect_to('home')
