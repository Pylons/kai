import logging

from openid import sreg
from openid.consumer import consumer
from pylons import app_globals, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest, secure, jsonify
from tw.mods.pylonshf import validate

from kai.lib.base import BaseController, render
from kai.lib.helpers import failure_flash, success_flash
from kai.model import Human, forms

log = logging.getLogger(__name__)

def proper_abort(end_action):
    if end_action == 'login':
        redirect_to('account_login')
    else:
        redirect_to('account_register')


class ConsumerController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True
        self.openid_session = session.get("openid_session", {})
    
    @rest.dispatch_on(POST='_handle_create')
    def create(Self):
        return render('/accounts/register.mako')
    
    @validate(form=forms.openid_login_form, error_handler='create')
    def _handle_create(self):
        return self._openid_login('register')
    
    @rest.dispatch_on(POST='_handle_login')
    def login(self):
        return render('/accounts/login.mako')
    
    @validate(form=forms.openid_login_form, error_handler='login')
    @secure.authenticate_form
    def _handle_login(self):
        return self._openid_login()
    
    def _openid_login(self, end_action='login'):
        openid_url = self.form_result['openid_identifier']
        if not openid_url:
            redirect_to('account_login')

        oidconsumer = consumer.Consumer(self.openid_session, app_globals.openid_store)
        try:
            authrequest = oidconsumer.begin(openid_url)
        except consumer.DiscoveryFailure, exc:
            err_msg = str(exc[0])
            if 'No usable OpenID' in err_msg:
                failure_flash('Invalid OpenID URL')
            else:
                failure_flash('Timeout for OpenID URL')
            proper_abort(end_action)
        
        if authrequest is None:
            failure_flash('No OpenID services found for <code>%s</code>' % openid_url)
            proper_abort(end_action)
        
        if end_action == 'register':
            sreg_request = sreg.SRegRequest(
                required=['fullname', 'email', 'timezone'],
                optional=['language']
            )
            authrequest.addExtension(sreg_request)
            session['openid_action'] = 'register'
        elif 'openid_action' in session:
            del session['openid_action']
        
        trust_root = url('home', qualified=True)
        return_to = url('openid_process', qualified=True)
        
        # OpenID 2.0 lets Providers request POST instead of redirect, this
        # checks for such a request.
        if authrequest.shouldSendRedirect():
            redirect_url = authrequest.redirectURL(realm=trust_root, 
                                                   return_to=return_to, 
                                                   immediate=False)
            session['openid_session'] = self.openid_session
            session.save()
            redirect_to(redirect_url)
        else:
            form_html = authrequest.formMarkup(
                realm=trust_root, return_to=return_to, immediate=False,
                form_tag_attrs={'id':'openid_message'})
            session['openid_session'] = self.openid_session
            session.save()
            return form_html
    
    def process(self):
        """Handle incoming redirect from OpenID Provider"""
        end_action = session.get('openid_action', 'login')
        
        oidconsumer = consumer.Consumer(self.openid_session, app_globals.openid_store)
        info = oidconsumer.complete(request.params, url('openid_process', qualified=True))
        if info.status == consumer.FAILURE and info.identity_url:
            fmt = "Verification of %s failed: %s"
            failure_flash(fmt % (info.identity_url, info.message))
        elif info.status == consumer.SUCCESS:
            openid_identity = info.identity_url
            if info.endpoint.canonicalID:
                # If it's an i-name, use the canonicalID as its secure even if
                # the old one is compromised
                openid_identity = info.endpoint.canonicalID
            
            # We've now verified a successful OpenID login, time to determine
            # how to dispatch it
            
            # First save their identity in the session, as several pages use 
            # this data
            session['openid_identity'] = openid_identity
            
            # Save off the session
            session.save()
            
            # First, if someone already has this openid, we log them in if
            # they've verified their email, otherwise we inform them to verify
            # their email address first
            users = list(Human.by_openid(self.db)[openid_identity])
            if users:
                user = users[0]
                if user.email_token:
                    failure_flash('You must verify your email before signing in.')
                    redirect_to('account_login')
                else:
                    user.process_login()
                    success_flash('You have logged into PylonsHQ')
                    redirect_to('home')
            
            # Second, if this is a registration request, present the rest of
            # registration process
            if session.get('openid_action', '') == 'register':
                sreg_response = sreg.SRegResponse.fromSuccessResponse(info)
                results = {}
                results['displayname'] = sreg_response['fullname']
                results['timezone'] = sreg_response['timezone']
                results['email_address'] = sreg_response['email']
                c.defaults = results
                c.openid = openid_identity
                return render('/accounts/register.mako')
            
            # The last option possible, is that the user is associating this
            # OpenID account with an existing account
            c.openid = openid_identity
            return render('/accounts/associate.mako')
        elif info.status == consumer.CANCEL:
            failure_flash('Verification cancelled')
        elif info.status == consumer.SETUP_NEEDED:
            if info.setup_url:
                c.message = '<a href=%s>Setup needed</a>' % info.setup_url
            else:
                # This means auth didn't succeed, but you're welcome to try
                # non-immediate mode.
                failure_flash('Setup needed')
        else:
            failure_flash('Verification failed.')
        session.delete()
        proper_abort(end_action)
