from formencode import All, Schema
from formencode.validators import FieldsMatch, UnicodeString, OneOf
from tw2 import forms
from tw2.core import DateTimeValidator, EmailValidator
import pytz

from kai.lib.highlight import langdict
from kai.model.validators import ExistingSnippetTitle, ExistingEmail, UniqueDisplayname, UniqueEmail, ValidLogin, ValidPassword


class FilteringSchema(Schema):
    filter_extra_fields = False
    allow_extra_fields = True
    ignore_key_missing = False


class AutoComplete(forms.TextField):
    template = 'mako:kai.model.widgets.autocomplete'


class SecureToken(forms.HiddenField):
    template = 'mako:kai.model.widgets.secure'


class BotsAreLame(forms.HiddenField):
    template = 'mako:kai.model.widgets.notabot'


class CommentForm(forms.TableForm):
    comment = forms.TextArea(
        validator = UnicodeString(not_empty=True))
    preview = forms.Button(
        name='Preview',
        value='Preview')
comment_form = CommentForm()


class SnippetForm(forms.TableForm):
    title = forms.TextField(
        validator = ExistingSnippetTitle(not_empty=True))
    description = forms.TextArea(
        help_text = "ONE paragraphs summarizing the snippet. NO FORMATTING IS APPLIED",
        validator = UnicodeString())
    content = forms.TextArea(
        help_text = "The full content of the snippet. Restructured Text formatting is used.",
        validator = UnicodeString(not_empty=True))
    tags = AutoComplete(
        validator = UnicodeString())
    preview = forms.Button(
        name='Preview',
        value='Preview')
snippet_form = SnippetForm()


class PastebinForm(forms.TableForm):
    title = forms.TextField(
        validator = UnicodeString(not_empty=True))
    language = forms.SingleSelectField(
        options = sorted(langdict.items(), cmp=lambda x,y: cmp(x[1], y[1])),
        validator = OneOf(langdict.keys(), not_empty=True))
    code = forms.TextArea(
        validator = UnicodeString(not_empty=True))
    tags = AutoComplete(
        validator = UnicodeString(not_empty=False))
    notabot = BotsAreLame(
        validator = UnicodeString(not_empty=True),
        value = 'most_likely')
pastebin_form = PastebinForm()


class NewArticleForm(forms.TableForm):
    title = forms.TextField(
        validator = UnicodeString(not_empty=True))
    summary = forms.TextField(
        validator = UnicodeString())
    body = forms.TextArea(
        rows = 15,
        validator = UnicodeString(not_empty=True))
    publish_date = forms.CalendarDateTimePicker(
        validator = DateTimeValidator())
    preview = forms.Button(
        name='Preview',
        value='Preview')
new_article_form = NewArticleForm()


class ChangePasswordForm(forms.TableForm):
    password = forms.PasswordField(
        validator = ValidPassword(not_empty=True))
    confirm_password = forms.PasswordField(
        validator = ValidPassword(not_empty=True))
    authentication_token = SecureToken()
    
    validator = FilteringSchema(
        chained_validators=[FieldsMatch('password', 'confirm_password')])
change_password_form = ChangePasswordForm()


class ForgotPasswordForm(forms.TableForm):
    email_address = forms.TextField(
        label_text = 'Email',
        validator = ExistingEmail(not_empty=True))
    authentication_token = SecureToken()
forgot_password_form = ForgotPasswordForm()


class LoginForm(forms.TableForm):
    email_address = forms.TextField(
        validator = EmailValidator(not_empty=True))
    password = forms.PasswordField(
        validator = UnicodeString(not_empty=True))
    authentication_token = SecureToken()
    validator = FilteringSchema(
        chained_validators=[ValidLogin(email='email_address', password='password')])
login_form = LoginForm()

class OpenIDLogin(forms.TableForm):
    openid_identifier = forms.TextField(
        label_text="OpenID Identifier",
        validator = UnicodeString(not_empty=True))
    authentication_token = SecureToken()
openid_login_form = OpenIDLogin()


class OpenIDRegistrationForm(forms.TableForm):
    displayname = forms.TextField(
        label_text = "Display Name",
        help_text = "Name that will appear when posting/commenting",
        validator = All(UnicodeString(not_empty=True), UniqueDisplayname()))
    email_address = forms.TextField(
        validator = All(EmailValidator(not_empty=True), UniqueEmail()))
    timezone = forms.SingleSelectField(
        options = pytz.common_timezones,
        validator = OneOf(pytz.common_timezones, not_empty=True))
openid_registration_form = OpenIDRegistrationForm()


class RegistrationForm(forms.TableForm):
    displayname = forms.TextField(
        label_text = "Display Name",
        help_text = "Name that will appear when posting/commenting",
        validator = All(UnicodeString(not_empty=True), UniqueDisplayname()))
    email_address = forms.TextField(
        validator = All(EmailValidator(not_empty=True), UniqueEmail()))
    timezone = forms.SingleSelectField(
        options = pytz.common_timezones,
        validator = OneOf(pytz.common_timezones, not_empty=True))
    password = forms.PasswordField(
        validator = ValidPassword(not_empty=True))
    confirm_password = forms.PasswordField(
        validator = ValidPassword(not_empty=True))
    authentication_token = SecureToken()
    validator = FilteringSchema(
        chained_validators=[FieldsMatch('password', 'confirm_password')])
registration_form = RegistrationForm()


